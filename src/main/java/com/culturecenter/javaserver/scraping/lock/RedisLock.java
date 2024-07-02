package com.culturecenter.javaserver.scraping.lock;


import com.culturecenter.javaserver.entity.Lectures;
import lombok.RequiredArgsConstructor;
import org.redisson.api.RBucket;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

import static com.culturecenter.javaserver.utils.Util.checking;

@Component
@RequiredArgsConstructor
public class RedisLock {

    private final RedissonClient client;

    public <T> T executeWithLock(String lockName, Supplier<T> supplier){
        RLock lock = client.getLock(lockName);
        boolean isLocked;
        try{
            while (!lock.tryLock(20, 30, TimeUnit.SECONDS)){
                isLocked = false;
            }
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


    public void setScrappingDelay (String lockName, List<Lectures> lectures){
        RBucket<String> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExists()) bucket.set(checking.javaObjectToJson(lectures), Duration.ofHours(1));
    }

    public List<Lectures> cachingScrappedLectures(String lockName){
        RBucket<String> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExists()) return null;
        String json = bucket.get();
        return checking.jsonToJavaObject(json);
    }
}
