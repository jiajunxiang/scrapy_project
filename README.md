# scrapy_project
基础学习scrapy框架，通过一些案例逐步解析框架的每个用法，由浅入深的理解scrapy<br>
main目录下的各个文件夹说明：<br>
learnscrapy是数据通过服务端渲染，适合基本爬虫练习，稍微有难度是含有登陆验证授权的处理。<br>
Ajax是通过 API 接口进行遍历的，所以使用总的页数进行循环就可以得到所有的起始 URL。<br>
Ajax_second没有起始 URL，通过字段count作为结束标志，自己构建URL。<br>
JWT和tooken一样都是身份验证的手段，两者区别在于前者的token是‘三段式’结构，由两个点连接起来的三个字符串。<br>

