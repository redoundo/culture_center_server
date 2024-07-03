package com.culturecenter.javaserver.scraping.scrapers;

import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.scraping.Command;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import com.culturecenter.javaserver.scraping.ScrapStatus;
import java.io.IOException;

/**
 * 홈플러스 사이트에서 강좌 상태를 스크래핑 해오는 과정
 */
public class HomePlusScraper implements Command {

    @Override
    public String parse(String url) {
        Document doc;
        try{
            doc = Jsoup.connect(url).get();
        } catch (IOException e) {
            System.out.println(e.getMessage());
            return null;
        }
        Element status = doc.selectFirst("#addLearnUser > div > div.decision > span > a > span");
        if(status == null) // 지점 문의 상태인 경우에는 a 태그가 존재하지 않는다.
            status = doc.selectFirst("#addLearnUser > div > div.decision > span.request.disabled > span > span");
        // 그래도 없는 경우에는 에러 반환.
        if (status == null) return "OVER"; //접수 기한이 종료된 게 오래 되었으면 페이지 자체가 없다. 그런 경우 OVER 반환.

        return ScrapStatus.HOMEPLUS_STATUS.checkStatus(status.text());
    }
}
