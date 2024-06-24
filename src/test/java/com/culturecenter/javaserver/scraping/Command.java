package com.culturecenter.javaserver.scraping;


public interface Command {

    public String parse(String url);
    public String extract();
}
