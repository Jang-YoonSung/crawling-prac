# 프로젝트명
> tv-조선 9시 뉴스 크롤링

자바 스크립트로 화면을 렌더링하는 tv-조선 9시 뉴스 페이지를 기간별로 크롤링하는 프로젝트

## 라이브러리 설치

```sh
pip install selenium requests beautifulsoup4
```

## 참고 사항

* selenium의 경우 사용 시 chrome driver 설치를 필요로 할 수 있음
  - 4.6 이후의 버전은 코드 실행 시 chrome driver를 자동으로 설치해줌  


## 사용 예제

```sh
result = crawling("2025-01-17", "2025-01-30")
```
위 코드의 기간을 설정한 후 코드 실행


## 기여 방법

1. (<https://github.com/Jang-YoonSung/crawling-prac/fork>)을 포크합니다.
2. (`git checkout -b crawling/test`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some test'`) 명령어로 커밋하세요.
4. (`git push origin crawling/test`) 명령어로 브랜치에 푸시하세요. 
5. 풀리퀘스트를 보내주세요.
