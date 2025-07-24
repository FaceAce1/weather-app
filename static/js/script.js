document.addEventListener('DOMContentLoaded', function() {
    const cityInput = document.getElementById('cityInput');
    const searchBtn = document.getElementById('searchBtn');
    const loadingElement = document.getElementById('loading');
    const errorElement = document.getElementById('error');
    const weatherResult = document.getElementById('weatherResult');
    
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
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
    
    function hideError() {
        errorElement.classList.add('hidden');
    }
    
    function showWeatherResult(data) {
        document.getElementById('cityName').textContent = data.city;
        document.getElementById('temperature').textContent = data.temperature;
        document.getElementById('condition').textContent = data.condition;
        document.getElementById('windDir').textContent = data.wind_dir;
        document.getElementById('windScale').textContent = data.wind_scale;
        document.getElementById('humidity').textContent = data.humidity;
        
        // 设置天气图标
        const iconUrl = `https://cdn.qweather.com/icons/${data.icon}.png`;
        document.getElementById('weatherIcon').src = iconUrl;
        document.getElementById('weatherIcon').alt = data.condition;
        
        weatherResult.classList.remove('hidden');
    }
    
    function hideWeatherResult() {
        weatherResult.classList.add('hidden');
    }
});