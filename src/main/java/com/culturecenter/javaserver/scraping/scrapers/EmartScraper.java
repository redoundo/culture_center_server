package com.culturecenter.javaserver.scraping.scrapers;

import com.culturecenter.javaserver.scraping.Command;
import com.culturecenter.javaserver.scraping.ScrapStatus;
import com.microsoft.playwright.Browser;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

/**
 * 이마트 사이트에서 강좌 상태를 스크래핑 해오는 과정
 */
public class EmartScraper implements Command {

    @Override
    public String parse(String url) {
        String state = null;
        try(Playwright playwright = Playwright.create()){
            try (Browser browser = playwright.chromium().launch()) {
                Page page = browser.newPage();
                page.navigate(url);
                if(page.isVisible("#container > div > div.clsdtl-info > div.clsdtl-vis > div > span.ico-txt-2")) {
                    String status = page.innerText("#container > div > div.clsdtl-info > div.clsdtl-vis > div > span.ico-txt-2");
                    state = ScrapStatus.EMART_STATUS.checkStatus(status);
                }else state = "OVER";
            } catch (Exception e) {
                System.out.println(e.getMessage());
                System.out.println("current url :   " + url);
            }
        }
        return state;
    }

}
