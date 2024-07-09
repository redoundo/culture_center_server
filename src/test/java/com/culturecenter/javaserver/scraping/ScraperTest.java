package com.culturecenter.javaserver.scraping;

import com.culturecenter.javaserver.dto.SearchConditions;
import com.culturecenter.javaserver.scraping.factory.ScraperFactory;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.redisson.Redisson;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import static com.culturecenter.javaserver.utils.Util.checking;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("분산 락 및 스크래핑 기능 테스트")
public class ScraperTest {
    private RedissonClient client;

    @BeforeEach
    public void setup() {
        Config config = new Config();
        config.useSingleServer()
                .setAddress("*********") // 개인 정보를 위해 삭제
                .setPassword("***") // 개인 정보를 위해 삭제
                .setUsername("default")
                .setConnectionPoolSize(30)
                .setConnectionMinimumIdleSize(5);
        client = Redisson.create(config);
    }

    @Test
    @Disabled("pass")
    @DisplayName("멀티 스레드 진행시 락 운용 과정이 어떤지 확인하기 위한 테스트")
    public void lockTest() throws InterruptedException {
        SearchConditions conditions = SearchConditions
                .builder()
                .centerName("HOMEPLUS")
                .build();
        String sql = checking.createSqlStatementByConditions(conditions);

        RLock lock = client.getLock(sql);
        int threadCount = 5; //thread 5 개
        ExecutorService executorService = Executors.newFixedThreadPool(threadCount); // thread 풀 생성
        CountDownLatch countDownLatch = new CountDownLatch(threadCount);
        for (int i = 0; i < threadCount; i++) {
            executorService.submit(() -> {
                try{
                    boolean isLocked = false; // 락 변수
                    System.out.println("락 요청 시작 전. 현재 락 상태:   " + isLocked);
                    // lease time 이 -1 인 경우 수동으로 unlock 을 진행해야 한다.
                    lock.lock( -1, TimeUnit.SECONDS); // 락 요청. 바로 가져오지 못하더라도 기다렸다가 가져온다.
                    isLocked = lock.isLocked(); // 락 상태 확인.
                    System.out.println("락 요청 완료... 현재 락 상태:  " + isLocked);
                    Thread.sleep(2000); // 작업으로 인한 락 해제 지연 대체
                    isLocked = lock.isLocked(); // 락 상태 확인
                    System.out.println("락 해제 2초 지연 완료. 현재 락 상태: " + isLocked);
                    assertTrue(isLocked);

                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                finally {
                    countDownLatch.countDown();
                    if(lock.isLocked() && lock.isHeldByCurrentThread()) lock.unlock(); // 반드시 lock 해제 필요
//                    if(lock.isLocked()) lock.unlockAsync(Thread.currentThread().getId());
                }
            });
        }
        countDownLatch.await();
        executorService.shutdown();
        client.shutdown();
    }

    @Test
    @Disabled("pass")
    @DisplayName("PlayWright 가 제대로 작동하는지 확인.")
    void contextLoads() {
        ScraperFactory factory = new ScraperFactory();
        Command command = factory.getScraper("EMART");
        String url = "https://www.cultureclub.emart.com/class/406CLlTvQ2024S2939";
        String status = command.parse(url);
        assertEquals(status, "OVER");
    }

    @Test
    @Disabled("pass")
    @DisplayName("jsoup 웹 스크래핑 작동 확인")
    void jsoupTest(){
        String url = "https://mschool.homeplus.co.kr/Lecture/Detail?LectureMasterID=9332494";
        try{
            Document doc = Jsoup.connect(url).get();
            if(doc != null) {
                Element status = doc.selectFirst("#addLearnUser > div > div.decision > span.request > a > span");
                assertNull(status);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
