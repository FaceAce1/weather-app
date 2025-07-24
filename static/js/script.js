document.addEventListener('DOMContentLoaded', function() {
    const locationInput = document.getElementById('cityInput'); // 修改为HTML中的实际ID
    const searchBtn = document.getElementById('searchBtn');
    const loadingIndicator = document.getElementById('loading'); // 修改为HTML中的实际ID
    const errorMessage = document.getElementById('error'); // 修改为HTML中的实际ID
    const weatherCards = document.querySelectorAll('.weather-card:not(#loading):not(#error)'); // 修改为HTML中的实际ID

    // 天气图标映射表
    const weatherIconMap = {
        "100": "fa-sun-o",      // 晴
        "101": "fa-cloud",      // 多云
        "102": "fa-cloud",      // 少云
        "103": "fa-cloud",      // 晴间多云
        "104": "fa-cloud",      // 阴
        "200": "fa-bolt",       // 雷暴
        "201": "fa-bolt",       // 强雷暴
        "202": "fa-bolt",       // 超强雷暴
        "203": "fa-bolt",       // 雷阵雨
        "204": "fa-bolt",       // 强雷阵雨
        "205": "fa-bolt",       // 超强雷阵雨
        "206": "fa-bolt",       // 雷阵雨伴有冰雹
        "207": "fa-bolt",       // 小到中雨
        "300": "fa-tint",       // 阵雨
        "301": "fa-tint",       // 强阵雨
        "302": "fa-tint",       // 特大阵雨
        "303": "fa-tint",       // 小雨
        "304": "fa-tint",       // 中雨
        "305": "fa-tint",       // 大雨
        "306": "fa-tint",       // 暴雨
        "307": "fa-tint",       // 大暴雨
        "308": "fa-tint",       // 特大暴雨
        "400": "fa-snowflake-o",// 小雪
        "401": "fa-snowflake-o",// 中雪
        "402": "fa-snowflake-o",// 大雪
        "403": "fa-snowflake-o",// 暴雪
        "404": "fa-snowflake-o",// 雨夹雪
        "500": "fa-cloud-fog",  // 雾
        "501": "fa-smog",       // 霾
        "502": "fa-wind",       // 沙尘暴
        "900": "fa-sun-o"       // 热
    };

    // 事件监听
    searchBtn.addEventListener('click', fetchWeatherData);
    locationInput.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            fetchWeatherData();
        }
    });

    // 初始加载示例数据
    // 删除初始调用，因为用户可能还没有输入城市
    // fetchWeatherData();

    function fetchWeatherData() {
        const location = locationInput.value.trim();
        if (!location) {
            alert('请输入城市名或经纬度');
            return;
        }

        showLoading();

        // 调用后端API
        fetch(`/api/weather?city=${encodeURIComponent(location)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('网络响应异常');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                displayWeatherData(data);
                hideLoading();
            })
            .catch(error => {
                console.error('获取天气数据失败:', error);
                showError(error.message);
            });
    }

    function displayWeatherData(data) {
        const now = data.now;
        const refer = data.refer || {};
        
        // 更新DOM元素
        document.getElementById('cityName').textContent = data.city || locationInput.value.trim();
        document.getElementById('updateTime').textContent = formatDateTime(data.updateTime);
        document.getElementById('obsTime').textContent = formatDateTime(now.obsTime);
        document.getElementById('temperature').textContent = now.temp;
        document.getElementById('condition').textContent = now.text; // 修改为HTML中的实际ID
        document.getElementById('feelsLike').textContent = `体感 ${now.feelsLike}°C`;
        document.getElementById('humidity').textContent = `湿度 ${now.humidity}%`;
        document.getElementById('windDir').innerHTML = `<i class="fa fa-location-arrow text-primary"></i> ${now.windDir}`;
        document.getElementById('wind360').textContent = now.wind360;
        document.getElementById('windScale').textContent = `${now.windScale}级`;
        document.getElementById('windSpeed').textContent = now.windSpeed;
        document.getElementById('pressure').innerHTML = `<i class="fa fa-dashboard text-primary"></i> ${now.pressure} hPa`;
        document.getElementById('visibility').innerHTML = `<i class="fa fa-eye text-primary"></i> ${now.vis} km`;
        document.getElementById('precip').textContent = `${now.precip} mm`;
        document.getElementById('cloud').textContent = now.cloud ? `${now.cloud}%` : '无数据';
        document.getElementById('dew').textContent = now.dew ? `${now.dew}°C` : '无数据';
        document.getElementById('sources').textContent = refer.sources ? refer.sources.join(', ') : '未知';

        // 更新天气图标
        updateWeatherIcon(now.icon);
        
        // 更新详情链接
        if (data.fxLink) {
            document.getElementById('detailLink').href = data.fxLink;
        }
    }

    function updateWeatherIcon(iconCode) {
        console.log('Weather Icon Code:', iconCode); // 调试：打印天气代码
        const iconElement = document.getElementById('weatherIcon').querySelector('i');
        const iconClass = weatherIconMap[iconCode] || 'fa-question-circle';
        
        iconElement.className = `fa ${iconClass}`;
    }

    function formatDateTime(dateTimeString) {
        if (!dateTimeString) return '未知时间';
        // 将"2020-06-30T22:00+08:00"格式化为"2020-06-30 22:00"
        return dateTimeString.replace('T', ' ').split('+')[0];
    }

    function showLoading() {
        // 隐藏所有天气卡片
        document.getElementById('weatherResult').classList.add('hidden');
        document.getElementById('detailedWeather').classList.add('hidden');
        errorMessage.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');
    }

    function hideLoading() {
        loadingIndicator.classList.add('hidden');
        errorMessage.classList.add('hidden');
        // 显示天气卡片
        document.getElementById('weatherResult').classList.remove('hidden');
        document.getElementById('detailedWeather').classList.remove('hidden');
    }

    function showError(message) {
        loadingIndicator.classList.add('hidden');
        document.getElementById('weatherResult').classList.add('hidden');
        document.getElementById('detailedWeather').classList.add('hidden');
        errorMessage.classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message || '获取天气数据失败';
    }
});