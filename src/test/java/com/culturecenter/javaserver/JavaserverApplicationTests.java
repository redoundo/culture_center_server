package com.culturecenter.javaserver;

import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
class JavaserverApplicationTests {

	@Test
	void contextLoads() {
		ScraperFactory factory = new ScraperFactory();
		Command command = factory.getScraper("EMART");
		String url = "https://www.cultureclub.emart.com/class/406CLlTvQ2024S2939";
		String status = command.parse(url);
		assertEquals(status, "OVER");
	}

}
