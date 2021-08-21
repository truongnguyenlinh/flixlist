# health home register[!] login recommendations friendlist [show_details header footer]
response=$(curl -s -o /dev/null -w "%{http_code}"  https://flixlist.tech/health)
if [ ${response} = 200 ]; then
        echo "health"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" https:/flixlist.tech/)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
response=$(curl -s -o /dev/null -w "%{http_code}" https://flixlist.tech/register)
if [ ${response} = 200 ]; then
        echo "register"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=user&password=passwd" https://flixlist.tech/register)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
response=$(curl -s -o /dev/null -w "%{http_code}" https://flixlist.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=user&password=passwd" https://flixlist.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "username=user&password=ic" https://flixlist.tech/login)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}"  https://flixlist.tech/logout)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST  https://flixlist.tech/recommendations)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST  https://flixlist.tech/friendlist)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST  https://flixlist.tech/show_details)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST  https://flixlist.tech/header)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0
response=$(curl -s -o /dev/null -w "%{http_code}" -X POST  https://flixlist.tech/footer)
if [ ${response} = 200 ]; then
        echo "success"
elif [ ${response} = 418 ]; then
        echo "input error"
elif [ ${response} = 501 ]; then
        echo "error"
else
        exit -1
fi
exit 0