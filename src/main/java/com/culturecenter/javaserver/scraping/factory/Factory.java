package com.culturecenter.javaserver.scraping.factory;

import com.culturecenter.javaserver.scraping.Command;

/**
 * 사이트마다 다른 스크래퍼가 필요하므로
 */
public interface Factory {
    Command getScraper(String center);
}
