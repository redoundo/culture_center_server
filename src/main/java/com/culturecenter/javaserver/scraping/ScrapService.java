package com.culturecenter.javaserver.scraping;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.dto.SearchResultsDto;
import com.culturecenter.javaserver.entity.Lectures;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import com.culturecenter.javaserver.scraping.lock.RedisLock;
import com.culturecenter.javaserver.service.ChangeService;
import com.culturecenter.javaserver.service.SelectService;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

import static com.culturecenter.javaserver.utils.Util.checking;
@Service
@RequiredArgsConstructor
public class ScrapService {
    private final ScraperFactory factory = new ScraperFactory();
    private final SelectService selectService;
    private final ChangeService changeService;
    private final RedisLock redisLock;

    @Async
    public SearchResultsDto checkAndUpdateStatus(SearchConditions conditions, String sql) {
        SearchResultsDto nullableLectures = redisLock.cachingScrappedLectures(sql);
        // redis 에 "SCRAP_KEY " + sql 과 동일한 키가 있으면 database 에서 가져올 필요 없이 redis 에서 cache 해온다.
        if (nullableLectures != null) return nullableLectures;
//        this.selectService.selectLectureByConditions(conditions);

        List<Lectures> lectures =  redisLock.executeWithLock(sql,
                () -> this.selectService.selectLectureByConditions(conditions));
        // 전체 페이지 수
        Integer total = selectService.lectureTotalCount(conditions);
        // "SCRAP_KEY " + sql 과 동일한 키가 있으면 웹 스크래핑을 진행하지 하지 않고 바로 반환. 1시간 동안 유지
        if(redisLock.rBucketExist(sql))
            return SearchResultsDto.builder()
                    .total(total)
                    .lectures(lectures)
                    .build();

        List<CompletableFuture<Lectures>> futureLectureList = lectures.stream().map(this::checkLectureStatus).toList();
        CompletableFuture<List<Lectures>> future =
                CompletableFuture.allOf(futureLectureList.toArray(new CompletableFuture[0]))
                        .thenApply(f -> futureLectureList.stream()
                                .map(CompletableFuture::join)
                                .collect(Collectors.toList()));

        List<Lectures> scrappedLectures = future.join();
        SearchResultsDto results = SearchResultsDto.builder()
                .total(total)
                .lectures(scrappedLectures)
                .build();
        redisLock.setScrappingDelay(sql, results); // 60분 동안 스크래핑 하지 않도록 설정 및 캐시 설정

        return results;
    }

    public CompletableFuture<Lectures> checkLectureStatus( Lectures lecture){
        return CompletableFuture.supplyAsync(() -> {
            Command command = this.factory.getScraper(lecture.getCenter());
            String status = command.parse(lecture.getUrl());
            if(status == null) return null;
            if(!lecture.getEnrollStatus().equals(status)) lecture.setEnrollStatus(status);
            this.changeService.updateEnrollStatus(lecture.getLectureId(), lecture.getEnrollStatus());
            return lecture;
        });
    }
}
