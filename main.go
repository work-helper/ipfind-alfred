package main

import (
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"strings"
	"text/template"
)

func main() {
	var result = `{
    "items": [{
        "uid": "1",
        "title": "Local  -->  {{.localIp}}",
        "subtitle": "{{.localHostname}}",
        "arg": "{{.localIp}}",
        "icon": {
            "path": "./icon.png"
        }
    },
    {
        "uid": "2",
        "title": "Net  -->  {{.netIp}}",
        "subtitle": "{{.netHostname}}",
        "arg": "{{.netIp}}",
        "icon": {
            "path": "./icon.png"
        }
    }]
}`
	m := map[string]string{}

	// 获取外网地址
	resp, err := http.Get("http://members.3322.org/dyndns/getip")
	if nil != err {
		panic(err)
	}
	defer resp.Body.Close()

	netIp, _ := ioutil.ReadAll(resp.Body)
	m["netIp"] = strings.ReplaceAll(string(netIp), "\n", "")
	m["netHostname"] = "外网地址"

	// 获取本机地址
	addrs, _ := net.InterfaceAddrs()
	for _, address := range addrs {
		// 检查ip地址判断是否回环地址
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				m["localIp"] = ipnet.IP.String()
				m["localHostname"] = "内网地址"
				break
			}

		}
	}

	tpl, _ := template.New("workflow").Parse(result)
	_ = tpl.Execute(os.Stdout, m)

}
