package com.culturecenter.javaserver.scraping;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.entity.Lectures;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import com.culturecenter.javaserver.service.ChangeService;
import com.culturecenter.javaserver.service.SelectService;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ScrapService {
    private final ScraperFactory factory;
    private final SelectService selectService;
    private final ChangeService changeService;

    @Async
    public List<Lectures> checkAndUpdateStatus(SearchConditions conditions) {
        List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
        List<CompletableFuture<Lectures>> futureLectureList = lectures.stream().map(this::checkLectureStatus).toList();
        CompletableFuture<List<Lectures>> future =
                CompletableFuture.allOf(futureLectureList.toArray(new CompletableFuture[0]))
                        .thenApply(f -> futureLectureList.stream()
                                .map(CompletableFuture::join)
                                .collect(Collectors.toList()));
        return future.join();
    }

    public CompletableFuture<Lectures> checkLectureStatus( Lectures lecture){
        return CompletableFuture.supplyAsync(() -> {
            Command command = this.factory.getScraper(lecture.getCenter());
            String status = command.parse(lecture.getUrl());
            if(!lecture.getEnrollStatus().equals(status)) lecture.setEnrollStatus(status);
            this.changeService.updateEnrollStatus(lecture.getLectureId(), lecture.getEnrollStatus());
            return lecture;
        });
    }
}
