package com.culturecenter.javaserver.scraping.scrapers;

import com.culturecenter.javaserver.error.CustomRuntimeException;
import com.culturecenter.javaserver.error.ErrorCode;
import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapStatus;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;

/**
 * 롯데 백화점 백화점 사이트에서 강좌 상태를 스크래핑 해오는 과정
 */
public class LotteScraper implements Command {

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
        Element status = this.doc.selectFirst("#wrap > div.cont_wrap > div > div.page_cont_area.no_padding > div.bg_inner.pd_bot > div > div > div.pin-spacer > div > div > div.shadow_div > div:nth-child(1) > div.pop_wrap > div > div.for_padding.on > div > div.pop_head > div.top_area > div.label_div > p:nth-child(1)");
        if (status == null) throw new CustomRuntimeException(ErrorCode.STATUS_UPDATE_ELEMENT_NOT_EXIST);
        return ScrapStatus.HOMEPLUS_STATUS.checkStatus(status.text());
    }
}
