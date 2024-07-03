package com.culturecenter.javaserver.scraping.scrapers;
import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapStatus;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;

public class ShinsegaeScraper implements Command {

    @Override
    public String parse(String url) {
        Document doc;
        try{
            doc = Jsoup.connect(url).get();
        } catch (IOException e) {
            System.out.println(e.getMessage());
            return null;
        }
        Element element = doc.selectFirst("#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(11) > td");
        // 3번째 a 태그에는 반드시 강좌 상태가 존재. 없으면 문제 발생했다는 의미
        if(element == null) return "OVER"; //접수 기한이 종료된 게 오래 되었으면 페이지 자체가 없다. 그런 경우 OVER 반환.
        return ScrapStatus.SHINSEGAE_STATUS.checkStatus(element.text());
    }
}
