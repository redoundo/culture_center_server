package com.culturecenter.javaserver.scraping.factory;

import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.scrapers.EmartScraper;

import java.util.HashMap;
import java.util.Map;

public class ScraperFactory implements Factory{

    public static Map<String , Command> cachedScraper = new HashMap<>();

    public ScraperFactory() {
        cachedScraper.put("EMART", new EmartScraper());
    }
    @Override
    public Command getScraper(String center) {
        if(cachedScraper.get(center) != null) return cachedScraper.get(center);
        else return null;
    }
}
