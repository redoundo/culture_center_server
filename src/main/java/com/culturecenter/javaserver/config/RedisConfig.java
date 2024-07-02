package com.culturecenter.javaserver.config;


import org.redisson.Redisson;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import org.redisson.spring.data.connection.RedissonConnectionFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.RedisStandaloneConfiguration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;

/**
 * redis configs
 */
@EnableCaching
@Configuration
@EnableRedisRepositories
@PropertySource("classpath:application.properties")
public class RedisConfig {

    @Value("${spring.data.redis.host}")
    private String host;

    @Value("${spring.data.redis.password}")
    private String password;

    @Value("${spring.data.redis.user}")
    private String userName;

    @Bean
    public RedissonClient redisClient(){
        Config config = new Config();
        config.useSingleServer()
                .setAddress(host)
                .setPassword(password)
                .setUsername(userName)
                .setDnsMonitoringInterval(-1);
        return Redisson.create(config);
    }


    /**
     * redis 연결
     * @return redisConnectionFactory
     */
    @Bean
    public RedisConnectionFactory redisConnectionFactory(RedissonClient client) {
        return new RedissonConnectionFactory(client);
    }
}
