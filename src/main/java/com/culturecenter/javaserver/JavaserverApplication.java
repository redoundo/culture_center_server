package com.culturecenter.javaserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

@EnableAspectJAutoProxy
@SpringBootApplication
public class JavaserverApplication {

	public static void main(String[] args) {
		SpringApplication.run(JavaserverApplication.class, args);
	}

}
