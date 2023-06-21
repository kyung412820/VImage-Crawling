<br>


# [Crawling] 비디오, 이미지 Crawling 툴

<br>

<h2>목차</h2>

 - [소개](#소개) 
 - [팀원](#팀원) 
 - [개발 환경](#개발-환경)
 - [사용 기술](#사용-기술)
 - [핵심 기능](#핵심-기능)
   - [Web](#web)
   - [Deep Learning](#deep-learning)
   - [Text Mining](#text-mining)
 - [Trouble Shooting](#trouble-shooting)


## 소개

**Crawling**는 필요에 따라 비디오의 아미지를 외부 사이트에서 크롤링하는 툴 입니다.<br>

## 팀원

<table>
   <tr>
    <td align="center"><b><a href="https://github.com/kyung412820">이경훈</a></b></td>
  <tr>
    <td align="center"><a href="https://github.com/kyung412820"><img src="https://avatars.githubusercontent.com/u/71320521?v=4" width="100px" /></a></td>
  </tr>
  <tr>
    <td align="center"><b>프로젝트 총괄</b></td>
</table>


## 개발 환경

 - Windows
 - Visual Code
 - GitHub



## 사용 기술 

- Library & Framework : requests, os, selenium, urllib, uuid, BeautifulSoup
- Language : Python



## 핵심 기능

### 크롤링

- requests를 이용하여 해당 url에 데이터를 요청하여 데이터를 수집합니다

  - 굳이 모든 데이터를 가져올 필요는 없으므로, 자신이 원하는 크기의 데이터만 수집하도록 response.headers.get로 요청하는 콘텐츠의 크기를 제단하여 필터링 했습니다.

- 폴더의 이름을 지정하기 위해 url에서 지정된 경로를 추출, 제목, 확장자를 반환하여 폴더의 이름을 구성합니다.

- 대용량 데이터를 크롤링 할 것 을 대비해 청크를 8kB정도로 맞추어 반복적으로 데이터를 파일에 기록합니다.

- BeautifulSoup를 이용하여 HTML문서에서 원하는 부분을 추출하였습니다.

  - src에서 image, video를 추출하도록 선언했습니다.

  - src가 외부 리소스의 url을 지정하는데 사용되다보니 이걸 중심으로 코드를 구성했습니다.



### javascript 요청

- 일반적으로 크롤링이 불가능한 경우 자바 스크립트 자체를 요청하는 방식을 사용했습니다.

  - chromedriver를 사용했습니다.

- chromedriver 객체를 상성하여 웹 페이지에 접속, html 문서를 직접 다운로드 하여 문제를 해결했습니다.

  - 기본적으로 해당 서버에 악 영향을 미칠 수 있음으로 wait을 설정하여 일정 대기시간을 부여하였습니다.



## Trouble Shooting

- 단순히 url을 복사 붙여넣기 하다보니 url의 https:가 선언이 안된 상태로 크롤링하는 문제가 있었습니다.

  - 위의 경우에만 video_url = "https:" + video_url를 사용해 문제를 해결했습니다.

- 유효하지 않은 문자가 포함되어 있는 경우 크롤링이 진행이 안되는 문제가 있었습니다.

  - 다른 사람의 조언으로 invalid_chars = r'\/:*?"<>|' 해당 코드들은 제거하도록 설정하였습니다.

