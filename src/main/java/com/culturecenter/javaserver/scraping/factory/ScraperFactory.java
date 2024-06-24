package com.culturecenter.javaserver.scraping.factory;

import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.scrapers.*;

import java.util.HashMap;
import java.util.Map;

public class ScraperFactory implements Factory{

    public static Map<String , Command> cachedScraper = new HashMap<>();

    public ScraperFactory() {
        cachedScraper.put("AKPLAZA", new AkplazaScraper());
        cachedScraper.put("EMART", new EmartScraper());
        cachedScraper.put("LOTTEMART", new LotteMartScraper());
        cachedScraper.put("LOTTE", new LotteScraper());
        cachedScraper.put("HYUNDAI", new HyundaiScraper());
        cachedScraper.put("GALLERIA", new GalleriaScraper());
        cachedScraper.put("HOMEPLUS", new HomePlusScraper());
        cachedScraper.put("SHINSEGAE", new ShinsegaeScraper());
    }

    @Override
    public Command getScraper(String center) {
        if(cachedScraper.get(center) != null) return cachedScraper.get(center);
        else return null;
    }
}
