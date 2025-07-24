document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('cityInput');
    const searchBtn = document.getElementById('searchBtn');
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const errorMessageElement = document.getElementById('errorMessage');
    const weatherResult = document.getElementById('weatherResult');
    
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

    // 搜索按钮点击事件
    searchBtn.addEventListener('click', searchWeather);
    
    // 回车键搜索
    cityInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchWeather();
        }
    });
    
    function searchWeather() {
        const city = cityInput.value.trim();
        
        if (!city) {
            showError('请输入城市名称');
            return;
        }
        
        // 显示加载状态
        showLoading();
        hideError();
        hideWeatherResult();
        
        // 调用API获取天气数据
        fetch(`/api/weather?city=${encodeURIComponent(city)}`)
            .then(response => response.json())
            .then(data => {
                hideLoading();
                
                if (data.error) {
                    showError(data.error);
                } else {
                    // 添加当前时间作为更新时间
                    data.updateTime = new Date().toISOString().replace('T', ' ').split('.')[0];
                    showWeatherResult(data);
                }
            })
            .catch(error => {
                hideLoading();
                showError('网络错误，请稍后重试');
                console.error('Error fetching weather data:', error);
            });
    }
    
    function showLoading() {
        loadingElement.classList.remove('hidden');
    }
    
    function hideLoading() {
        loadingElement.classList.add('hidden');
    }
    
    function showError(message) {
        errorMessageElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
    
    function hideError() {
        errorElement.classList.add('hidden');
    }
    
    function showWeatherResult(data) {
        // 更新DOM元素
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('updateTime').textContent = data.updateTime;
        document.getElementById('temperature').textContent = data.temperature;
        document.getElementById('condition').textContent = data.condition;
        document.getElementById('feelsLike').textContent = `体感 ${data.temperature}°C`;
        document.getElementById('humidity').textContent = `湿度 ${data.humidity}%`;
        document.getElementById('windDir').innerHTML = `<i class="fa fa-location-arrow text-primary"></i> ${data.wind_dir}`;
        document.getElementById('windScale').textContent = `${data.wind_scale}级`;
        document.getElementById('humidityValue').innerHTML = `<i class="fa fa-tint text-primary"></i> ${data.humidity}%`;

        // 更新天气图标
        updateWeatherIcon(data.icon);
        
        weatherResult.classList.remove('hidden');
    }
    
    function updateWeatherIcon(iconCode) {
        const iconElement = document.getElementById('weatherIcon').querySelector('i');
        const iconClass = weatherIconMap[iconCode] || 'fa-question-circle';
        
        // 移除所有图标类
        iconElement.className = '';
        // 添加新的图标类
        iconElement.className = `fa ${iconClass}`;
    }
    
    function hideWeatherResult() {
        weatherResult.classList.add('hidden');
    }
});