package com.culturecenter.javaserver.scraping.lock;


import com.culturecenter.javaserver.dto.SearchResultsDto;
import lombok.RequiredArgsConstructor;
import org.redisson.api.RBucket;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

import static com.culturecenter.javaserver.utils.Util.checking;

@Component
@RequiredArgsConstructor
public class RedisLock {

    private final RedissonClient client;

    public <T> T executeWithLock(String lockName, Supplier<T> supplier){
        RLock lock = client.getLock(lockName);
//        boolean isLocked; // 락을 가지고 있지 않은게 default
        try{
//            while (!lock.tryLock(20, -1, TimeUnit.SECONDS)){
//                // 락을 가져오는 데 실패한 경우, 즉 스크래핑이 진행중일 때는 락을 가져올 수 있을 때까지 기다린다.
//                isLocked = false;
//            }
//            isLocked = lock.isLocked();
            lock.lock(-1, TimeUnit.SECONDS);
            return supplier.get();

        }
//        catch (InterruptedException e) {
//            throw new RuntimeException(e);
//        }
        finally {
            if(lock.isHeldByCurrentThread()) lock.unlock();
        }
    }

    public boolean rBucketExist(String lockName){
        RBucket<Object> bucket = client.getBucket("SCRAP_KEY " + lockName);
        return bucket.isExists();
    }


    public void setScrappingDelay (String lockName, SearchResultsDto results){
        RBucket<String> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExists()) bucket.set(checking.javaObjectToJson(results), Duration.ofHours(1));
    }

    public SearchResultsDto cachingScrappedLectures(String lockName){
        RBucket<String> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExists()) return null;
        String json = bucket.get();
        return checking.jsonToJavaObject(json);
    }
}
