package com.culturecenter.javaserver.service;

import com.culturecenter.javaserver.dto.SearchConditions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;

import static com.culturecenter.javaserver.utils.Util.checking;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("캐시 서비스 테스트 진행")
public class CacheServiceTest {
    private RedissonClient client;
    private CacheService cacheService;

    @BeforeEach
    public void setup() {
        Config config = new Config();
        config.useSingleServer()
                .setAddress("redis://redis-10155.c54.ap-northeast-1-2.ec2.redns.redis-cloud.com:10155") // 개인 정보를 위해 삭제
                .setPassword("Jj3ns0BvunMyKb3ZQ26ZIHIqkiwx8mli") // 개인 정보를 위해 삭제
                .setUsername("default")
                .setConnectionPoolSize(30)
                .setConnectionMinimumIdleSize(5);
        client = Redisson.create(config);
        cacheService = new CacheService(client);
    }


}
