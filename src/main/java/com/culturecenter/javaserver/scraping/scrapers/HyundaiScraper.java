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
 * 현대 백화점 사이트에서 강좌 상태를 스크래핑 해오는 과정
 */
public class HyundaiScraper implements Command {
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
        //대기 신청: #selectedCrsBill > button.sbtn.black > span
        //마감 #selectedCrsBill > button:nth-child(7) > span
        // 중간 신청: #selectedCrsBill > button.sbtn.black > span
        // 신청 하기 #selectedCrsBill > button.sbtn.black > span
        Element status = this.doc.selectFirst("#selectedCrsBill > button.sbtn.black > span");
        if(status == null) // 처음의 css selector 로 가져올 수가 없다면 마감 상태일 수도 있으므로, 확인
            status = this.doc.selectFirst("#selectedCrsBill > button:nth-child(7) > span");
        // 그래도 없는 경우에는 에러 반환.
        if (status == null) throw new CustomRuntimeException(ErrorCode.STATUS_UPDATE_ELEMENT_NOT_EXIST);
        return ScrapStatus.HYUNDAI_STATUS.checkStatus(status.text());
    }
}
