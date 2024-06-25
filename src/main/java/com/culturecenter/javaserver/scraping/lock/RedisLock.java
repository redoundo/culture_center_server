package com.culturecenter.javaserver.scraping.lock;


import lombok.RequiredArgsConstructor;
import org.redisson.api.RBucket;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;

import java.time.Duration;
import java.time.Instant;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

@RequiredArgsConstructor
public class RedisLock {

    private final RedissonClient client;

    public <T> T executeWithLock(String lockName, Supplier<T> supplier){
        RLock lock = client.getLock(lockName);
        boolean isLocked = false;
        try{
            isLocked = lock.tryLock(10, 30, TimeUnit.SECONDS);
            if(isLocked){
                return supplier.get();
            } else throw new RuntimeException("time out exception!!");

        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        finally {
            lock.unlock();
        }
    }

    public boolean rBucketExist(String lockName){
        RBucket<Object> bucket = client.getBucket("SCRAP_KEY " + lockName);
        return bucket.isExists();
    }


    public void setScrappingDelay (String lockName){
        RBucket<Object> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExists()) bucket.set(lockName, Duration.ofHours(1));
    }
}
