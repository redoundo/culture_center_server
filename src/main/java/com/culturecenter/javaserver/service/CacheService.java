package com.culturecenter.javaserver.service;

import lombok.RequiredArgsConstructor;
import org.redisson.api.RBucket;
import org.redisson.api.RedissonClient;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.util.concurrent.CompletableFuture;

import static com.culturecenter.javaserver.utils.Util.checking;

@Service
@RequiredArgsConstructor
public class CacheService {
    private final RedissonClient client;

    /**
     * 키로 키 값을 가져온다. 
     * @param key 키 이름 (보통 sql 문)
     * @param clazz 저장된 키 값의 타입
     * @return java 객체로 변경한 뒤 반환
     * @param <T> 불특정 타입
     */
    public <T> T getCacheValue(String key, Class<T> clazz){
        RBucket<String> bucket = this.client.getBucket(key);
        if (bucket.isExistsAsync().toCompletableFuture().join()) {
            CompletableFuture<String> value = bucket.getAsync().toCompletableFuture();
            return checking.jsonToJavaObject(value.join(), clazz);
        }
        else return null;
    }

    /**
     * redis 에 동일한 키가 없다면 저장. 동일한 키가 있지만 값이 다르다면 값 업데이트. 동일한 키와 값이라면 패스.
     * @param key 키 이름
     * @param value 저장할 키 값
     * @param clazz 저장할 값의 class 타입
     * @param <T> 불특정 타입
     */
    public <T> void putCacheValue(String key, T value, Class<T> clazz){
        RBucket<String> bucket = this.client.getBucket(key);
        // redis 에 동일한 키가 존재하지 않는 경우
        if(!bucket.isExistsAsync().toCompletableFuture().join()){
            String result = checking.javaObjectToJson(value);
            bucket.setAsync(result, Duration.ofMinutes(30)).toCompletableFuture().join();
            return;
        }
        // 이미 redis 에 동일한 키로 존재하는 경우 아래 내용 진행
        T existValue = this.getCacheValue(key, clazz);
        // 동일한 키로 가져온 값이 저장해야할 내용과 동일한 경우, return
        if(checking.sameContentObject(existValue, value)) return;

        //현재 값을 ObjectMapper 를 이용해 문자열로 변환.
        String existResult = checking.javaObjectToJson(existValue);
        // 동일한 키 값으로 가져온 값이 현재 값과 다를 경우 다시 저장.
        bucket.setAsync(existResult, Duration.ofMinutes(30)).toCompletableFuture().join();
    }

    /**
     * duration 시간을 설정할 수 있게 오버로딩
     * @param key 키 이름
     * @param value 저장할 키 값
     * @param clazz 저장할 값의 class 타입
     * @param duration ttl 시간
     * @param <T> 불특정 타입
     */
    public <T> void putCacheValue(String key, T value, Class<T> clazz, Integer duration){
        RBucket<String> bucket = this.client.getBucket(key);
        // redis 에 동일한 키가 존재하지 않는 경우
        if(!bucket.isExistsAsync().toCompletableFuture().join()){
            String result = checking.javaObjectToJson(value);
            bucket.setAsync(result, Duration.ofMinutes(duration.longValue())).toCompletableFuture().join();
            return;
        }
        // 이미 redis 에 동일한 키로 존재하는 경우 아래 내용 진행
        T existValue = this.getCacheValue(key, clazz);
        // 동일한 키로 가져온 값이 저장해야할 내용과 동일한 경우, return
        if(checking.sameContentObject(existValue, value)) return;

        //현재 값을 ObjectMapper 를 이용해 문자열로 변환.
        String existResult = checking.javaObjectToJson(existValue);
        // 동일한 키 값으로 가져온 값이 현재 값과 다를 경우 다시 저장.
        bucket.setAsync(existResult, Duration.ofMinutes(duration.longValue())).toCompletableFuture().join();
    }

}
