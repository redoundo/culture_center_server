package com.culturecenter.javaserver;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.entity.Lectures;
import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapService;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;

import com.culturecenter.javaserver.scraping.lock.RedisLock;
import com.culturecenter.javaserver.service.SelectService;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;
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
	void contextLoads() {
		ScraperFactory factory = new ScraperFactory();
		Command command = factory.getScraper("EMART");
		String url = "https://www.cultureclub.emart.com/class/406CLlTvQ2024S2939";
		String status = command.parse(url);
		assertEquals(status, "OVER");
	}

	@Test
	@DisplayName("jsoup 웹 스크래핑 작동 확인")
	void jsoupTest(){
		String url = "https://mschool.homeplus.co.kr/Lecture/Detail?LectureMasterID=9332494";
		try{
			Document doc = Jsoup.connect(url).get();
			if(doc != null) {
				Element status = doc.selectFirst("#addLearnUser > div > div.decision > span.request > a > span");
                assertNull(status);
			}
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}


	@Disabled("pass")
	@Test
	@DisplayName("redisson 이 제대로 작동하는지, 값이 제대로 가지고 와지는지, 병렬적으로 처리가 잘 되는지 확인.")
	void lockTest(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		assertEquals(lectures, this.scrapService.checkAndUpdateStatus(conditions));
	}

	@Test
	@DisplayName("java object to json && json to java object")
	void javaObjectAndJson(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		List<Lectures> cachedLectures = this.scrapService.checkAndUpdateStatus(conditions);
		assertEquals(checking.javaObjectToJson(lectures), checking.javaObjectToJson(cachedLectures));
	}

	@Test
	@Disabled("pass")
	@DisplayName("json to java object")
	void jsonToJavaObject(){
		SearchConditions conditions = SearchConditions
				.builder()
				.centerName("HOMEPLUS")
				.build();
		List<Lectures> lectures = this.selectService.selectLectureByConditions(conditions);
		List<Lectures> cachedLectures = this.redisLock.cachingScrappedLectures("SELECT * FROM lectures  WHERE center='HOMEPLUS' LIMIT 0,16;");
		assertEquals(lectures, cachedLectures);
	}

}
