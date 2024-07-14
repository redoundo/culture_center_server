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
        try{
            lock.lock(-1, TimeUnit.SECONDS);
            return supplier.get();
        }
        finally {
            if(lock.isHeldByCurrentThread()) lock.unlock();
        }
    }

//    public boolean rBucketExist(String lockName){
//        RBucket<Object> bucket = client.getBucket("SCRAP_KEY " + lockName);
//        return bucket.isExists();
//    }

    public boolean rBucketExist(String lockName){
        RBucket<Object> bucket = client.getBucket("SCRAP_KEY " + lockName);
        return bucket.isExistsAsync().toCompletableFuture().join();
    }


    public <T> void setCacheDelay(String lockName, T results, Integer duration){
        RBucket<String> bucket = client.getBucket(lockName);
        if(!bucket.isExists())
            bucket.setAsync(checking.javaObjectToJson(results), Duration.ofMinutes(duration.longValue())).toCompletableFuture().join();
    }

    public SearchResultsDto cachingScrappedLectures(String lockName){
        RBucket<String> bucket = client.getBucket("SCRAP_KEY " + lockName);
        if(!bucket.isExistsAsync().toCompletableFuture().join()) return null;
        String json = bucket.getAsync().toCompletableFuture().join();
        return checking.jsonToJavaObject(json, SearchResultsDto.class);
    }
}
