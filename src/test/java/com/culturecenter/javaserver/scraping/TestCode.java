package com.culturecenter.javaserver.scraping;
import static org.junit.jupiter.api.Assertions.assertEquals;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import org.junit.jupiter.api.Test;

public class TestCode {
    private  final ScraperFactory factory;

    public TestCode(ScraperFactory factory) {
        this.factory = factory;
    }

    @Test
    public void PlaywrightTestCode(){
        String url = "https://www.cultureclub.emart.com/class/406CLlTvQ2024S2939";
        Command command = factory.getScraper("EMART");
        String status = command.parse(url);
        assertEquals(status, "OVER");
    }
}
