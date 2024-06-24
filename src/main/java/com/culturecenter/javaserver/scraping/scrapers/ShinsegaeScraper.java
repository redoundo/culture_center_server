package com.culturecenter.javaserver.scraping.scrapers;

import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapStatus;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;

public class ShinsegaeScraper implements Command {

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
        Element element = this.doc.selectFirst("#inContent > div.wrap.mb70 > div.detail_form2 > table > tbody > tr:nth-child(11) > td");
        // 3번째 a 태그에는 반드시 강좌 상태가 존재. 없으면 문제 발생했다는 의미
        if(element == null) throw new CustomRuntimeException(ErrorCode.STATUS_UPDATE_ELEMENT_NOT_EXIST);
        return ScrapStatus.SHINSEGAE_STATUS.checkStatus(element.text());
    }
}
