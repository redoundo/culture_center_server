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

    private Page page;

    @Override
    public String parse(String url) {
        String state = null;
        try(Playwright playwright = Playwright.create()){
            try (Browser browser = playwright.chromium().launch()) {
                this.page = browser.newPage();
                this.page.navigate(url);
                state = this.extract();
            }
        }
        return state;
    }

    @Override
    public String extract() {
        String status = this.page.innerText("#container > div > div.clsdtl-info > div.clsdtl-vis > div > span.ico-txt-2");
        return ScrapStatus.EMART_STATUS.checkStatus(status);
    }
}
