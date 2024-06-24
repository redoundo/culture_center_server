package com.culturecenter.javaserver.scraping.scrapers;

import com.culturecenter.javaserver.scraping.Command;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;

/**
 * akplaza 사이트에서 강좌 상태를 스크래핑 해오는 과정
 */
public class AkplazaScraper implements Command {
    private Document doc;

    @Override
    public String parse(String url) {
        try{
            this.doc = Jsoup.connect(url).get();
        } catch (IOException e) {
            System.out.println(e.getMessage());
            this.doc = null;
        }
        return this.extract();
    }

    @Override
    public String extract() {
        Element element = this.doc.selectFirst("body > div.all-wrap > div.cours-sec.cours-sec01.bg-gray > div > div > div.btn-right > a.btn.btn02");
        if(element == null) return "OVER"; // 찾으려고 하는 element 가 없으면 그냥 접수 종료된 상태.
        return "ING";
    }

}
