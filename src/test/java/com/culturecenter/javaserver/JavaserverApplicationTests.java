package com.culturecenter.javaserver;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.dto.SearchResultsDto;
import com.culturecenter.javaserver.entity.Lectures;
import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapService;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import com.culturecenter.javaserver.scraping.lock.RedisLock;
import com.culturecenter.javaserver.service.SelectService;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static com.culturecenter.javaserver.utils.Util.checking;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

@SpringBootTest
class JavaserverApplicationTests {
	@Autowired
	private ScrapService scrapService;
	@Autowired
	private SelectService selectService;
	@Autowired
	private RedisLock redisLock;

	@Test
	@DisplayName("웹 스크래핑 진행 용 test. 웹 스크래핑 과정 및 redis 저장 과정에서 문제가 없는지 확인.")
	@Disabled("pass")
	void lockTest(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		SearchResultsDto dto = SearchResultsDto.builder()
				.total(selectService.lectureTotalCount(conditions))
				.lectures(lectures)
				.build();

		String sql = checking.createSqlStatementByConditions(conditions);

		assertEquals(dto, this.scrapService.checkAndUpdateStatus(conditions, sql));
	}

	@Disabled("pass")
	@Test
	@DisplayName("redis 캐싱 처리 과정 확인 - java object to json")
	void javaObjectAndJson(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		// db 에 저장된 내용. scrap 후 나올 거라 생각하는 예상 값.
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		SearchResultsDto dto = SearchResultsDto.builder()
				.total(selectService.lectureTotalCount(conditions))
				.lectures(lectures)
				.build();
		// scrapping 을 진행한 뒤 가져온 값. 실제 값
		String sql = checking.createSqlStatementByConditions(conditions);
		SearchResultsDto results = this.scrapService.checkAndUpdateStatus(conditions, sql);

		assertEquals(checking.javaObjectToJson(dto), checking.javaObjectToJson(results));
	}

	@Test
	@DisplayName("redis 캐싱 json 처리 과정 확인 json to java object")
	@Disabled("pass")
	void jsonToJavaObject(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		SearchResultsDto dto = SearchResultsDto.builder()
				.total(selectService.lectureTotalCount(conditions))
				.lectures(lectures)
				.build();
		SearchResultsDto cachedLectures = this.redisLock.cachingScrappedLectures("SELECT * FROM lectures  WHERE center='HOMEPLUS' LIMIT 0,16;");
		assertEquals(dto, cachedLectures);
	}
	@Test
	@DisplayName("PlayWright 가 제대로 작동하는지 확인.")
	void contextLoads() {
		ScraperFactory factory = new ScraperFactory();
		Command command = factory.getScraper("EMART");
		String url = "https://www.cultureclub.emart.com/class/406hC3jsQ2024S2947";
		String status = command.parse(url);
		assertEquals(status, "OVER");
	}

	@Test
	@DisplayName("k6 로 테스트 테스트 하는 도중에 에러가 난 다는 것을 알게 되어 테스트 진행")
	@Disabled("pass")
	void JpqlTest(){
		SearchConditions conditions = SearchConditions
				.builder()
				.page(2)
				.centerName("AKPLAZA")
				.keyword("베이비")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
        assertEquals(List.of(), lectures);
	}

	@Test
	@DisplayName("존재하지 않는 lectureId 에 대해서 어떻게 반응하는지 확인")
	@Disabled("pass")
	void GetByLectureId(){
		Lectures lecture = this.selectService.selectLectureByLectureId(9859);
        assertNull(lecture);
	}

	@Test
	@DisplayName("페이지네이션 확인")
	@Disabled("pass")
	void pagination(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.page(2)
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		assertEquals(32, lectures.size());
	}
	
	@Test
	@DisplayName("@Async 없이 스크래핑 진행")
	@Disabled("pass")
	void NoAsync(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		String sql = checking.createSqlStatementByConditions(conditions);
		SearchResultsDto results = this.scrapService.checkAndUpdateStatus(conditions, sql);
 		assertEquals(selectService.lectureTotalCount(conditions), results.getTotal());
	}

	@Test
	@DisplayName("keyword 요청 에러 확인")
	void keywordTest(){
		SearchConditions conditions = SearchConditions.builder().page(4).build();
		Integer total = this.selectService.lectureTotalCount(conditions);
		assertEquals(64, total);
	}


}
