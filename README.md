# Current state of the project
Parser code: `parser.py`
Image preprocessing and augmentation: `preprocessing.ipynb`
Baseline training: `baseline.ipynb`
Dataset: [https://drive.google.com/file/d/1ypyhndsupRkYZ509cFzEi8mKTiMPPoSW/view?usp=sharing](https://drive.google.com/file/d/1ypyhndsupRkYZ509cFzEi8mKTiMPPoSW/view?usp=sharing)
Wandb dashboard: https://wandb.ai/dushamishkin/baseline?workspace=user-dushamishkin


# Baseline
# Сбор данных

Файл: `parser.py`

Сбор данных осуществлялся путем парсинга сайта базы данных Тайваньского Национального Университета ([https://xiaoxue.iis.sinica.edu.tw/jinwen](https://xiaoxue.iis.sinica.edu.tw/jinwen)). Непосредственно парсинг выполнялся с помощью библиотеки selenium, т.к. структура веб-страниц была динамической, необходимо было взаимодействовать с различными кнопками и текстовыми полями. Код для парсинга расположен в файле parser.py.

Проблемы, возникшие во время парсинга:

- Проблемы с доступом бота к сайту. Система безопасности отколняла любые роботоизированные действия и банила ip;
- Сложности с навигацией по сайту и взаимодействию с javascript элементами;
- Наличие пустых классов. Данная проблема решается на этапе преодобработки;

**В результате** парсинга был получен датасет с изображениями в формате png, распределенными по папкам в соответствии с принадлежностью к номеру класса. Классов: 3578, из них около 20 пустые и будут удалены во время предобработки. Количество изображений в классе варьируется от 1 до 50, в каждом классе могут присутствовать 1-3 нерелевантных (не являющихся цзиньвэнями) изображения - также будут удалены во время предобработки. Общее количество изображений: 26.186, вес 65 мб.

Ссылка на датасет: [https://drive.google.com/file/d/1ypyhndsupRkYZ509cFzEi8mKTiMPPoSW/view?usp=sharing](https://drive.google.com/file/d/1ypyhndsupRkYZ509cFzEi8mKTiMPPoSW/view?usp=sharing)

# Предобработка

Файл: `preprocessing.ipynb`

### Задачи и методы

1. Произвести чистку датасета - удалить пустые классы и нерелевантные изображения
    1. Отсутствует код, но он элементарный
2. Конвертировать изображения из RGBA (A - канал прозрачности) в RGB, из png в jpg
    1. `pure_pil_alpha_to_color()`
3. Удалить шум с изображений с помощью гауссовского размытия
    1. `apply_gauss()`
4. Инвертировать картинки, на которых иероглифы изображены белым по черному, в формат черного по белому (см. пример)
    1. `is_too_black()`

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/57a8dd0a-f87c-450e-bb51-af84e1629a71/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230106%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230106T191308Z&X-Amz-Expires=86400&X-Amz-Signature=010e74d0aede70555108e210b7d1c56c775f9b104de86e1b4efc8ec85935f826&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)

![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/e546dfbe-b292-4024-a25e-ffdc5a0477d8/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230106%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230106T191244Z&X-Amz-Expires=86400&X-Amz-Signature=6caca6a0f9940391917e22a5805e1a1925565b7093a8e5b172ffc75a864b4ae2&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22Untitled.png%22&x-id=GetObject)

1. Избавиться от черных полос, возникающих при таком инвертировании
    1. `crop_borders()` + вспомогательные функции
    
    ![Untitled](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/637cd2a9-c987-43c3-a065-123ecb7dc418/with_borders.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230106%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230106T192758Z&X-Amz-Expires=86400&X-Amz-Signature=0175645979561e7708033da26b464d806f2f271724c23a6dd6b8fb4862759570&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22with_borders.jpg%22&x-id=GetObject)
2. Аугментировать изображения 4 различными способами одновременно:
    1. Fog, blur, noise, brightness and contrast
    2. Blur, noise, brightness, rotation, scaling
    3. Blur, noise, brightness, geometric transform
    4. Blur, noise, brightness and perspective

### Результаты

В результате преодобработки и аугментации получен следующий датасет:

1. 3,262 класса
2. 519,820 изображений
3. 634 мб размер

Ссылка на датасет: [https://drive.google.com/file/d/18QgdlNeUVViaXzrc3Un34V6xx2n6QudG/view?usp=sharing](https://drive.google.com/file/d/18QgdlNeUVViaXzrc3Un34V6xx2n6QudG/view?usp=sharing)

### Возникшие проблемы

1. Некоторые изображения инвертируются по ошибке, т.к. функция все равно считает их “слишком черными”. На самом деле, не сильно страшно, т.к. таких случаев не особо много
2. Аугментация не полностью решает проблему дисбаланса классов, а может быть даже и ухудшает ее. Все потому, что каждое изображение умножается на 4. Следовательно, для больших классов число изображений становится 50*4=200, а для маленьких всего 1*4=4.

# Бейзлайн

В принципе, тут расписывать особо нечего. Выполнен с помощью фреймворка pytorch lightning, для лога метрик использовал wandb. В качестве бейзлайн модели выбрал resnet18

### Результаты

- resnet18, SGD, lr=0.001, L2=0, momentum=0.9 – 0.94 (дальше колаб не дал доучить)

- resnet18, Adam, lr=0.001, L2=0 – validation accuracy 0.96

### Проблемы

Сразу можно заметить, что считаю accuracy. Все дело в том, что нужные метрики (precision, recall и f1) работают очень плохо с таким серьезным дисбалансом классов. При правильном их подсчете (macro) в среднем выдают значения >0.005. При micro подсчете, работает еще хуже. К примеру, f1 превращается в accuracy (можно заметить в графиках wandb). С этим мне нужна будет помощь. 

Ссылка на тетрадку: [https://colab.research.google.com/drive/1_8OVWd6GOAieFBYDJAT7GKF-hQzXVKY-?usp=sharing](https://colab.research.google.com/drive/1_8OVWd6GOAieFBYDJAT7GKF-hQzXVKY-?usp=sharing)

Ссылка на проект в wandb: [https://wandb.ai/dushamishkin/baseline](https://wandb.ai/dushamishkin/baseline)
***
---
***
# Предложение о курсовой работе
# Тема: **классификация древнекитайских иероглифов на бронзовых сосудах**

# Определение цзиньвэнь 金文
Цзиньвэнь 金文 jīn wén – надписи, выполненные на древних китайских бронзовых изделиях, датируются эпохами Шан (1554-1046 гг. до н. э.) и Чжоу (1045-221 гг. до н. э.)

![JinWen_example](https://upload.wikimedia.org/wikipedia/commons/2/27/LishuHuashanmiao.jpg "Пример цзиньвэнь")

Подавляющее число цзиньвэней являются прямыми предшественниками современных китайских иероглифов. Ниже продемонстрирована эволюция иероглифа 足 от цзиньвэнь до современного образа

![jinwen-to-modern](https://img01.yzcdn.cn/upload_files/2017/02/20/FtrwinMVN3lgGmxdgsHw1vj3VwjK.jpg!730x0.jpg "Эволюция иероглифа от цзиньвэнь до современного образа")

# Цели проекта
**Основная.** Обучить модель, классифицирующую иероглифы цзиньвэнь. Задача многоклассовой классификации на 3069 классов. На вход подается изображение 28х28, содержащее иероглиф, модель предсказывает номер класса в соответствии с сайтом https://xiaoxue.iis.sinica.edu.tw/jinwen (о нем будет рассказано ниже)

**Возможные дополнительные задачи.** При достижении хорошего качества у классификатора могут быть поставлены следующие цели:
- **Имплементация детектирования иероглифов**. На вход подается не 1 иероглиф, а изображение непосредственно сосуда/скана надписи, модель предсказывает области иероглифов и их классы. Пример, как это сделать [тут](https://pyimagesearch.com/2020/06/22/turning-any-cnn-image-classifier-into-an-object-detector-with-keras-tensorflow-and-opencv/)
- **Создание веб-сервиса**, в котором пользователь рисует иероглиф на холсте, а модель предсказывает класс. Пример [тут](https://towardsdatascience.com/develop-an-interactive-drawing-recognition-app-based-on-cnn-deploy-it-with-flask-95a805de10c0)

# Методы
- Составление датасета осуществляется путем парсинга базы данных Тайваньского Национального Университета: https://xiaoxue.iis.sinica.edu.tw/jinwen (*есть код, надо заново спарсить, чтобы получить актуальные данные)
- Препоцессинг изображений включает в себя
    - Ручное удаление лишних элементов-изображений, загруженных во время парсинга (избавиться от них автоматически, к сожалению, нельзя)
    - Конвертация RGBA to RGB (*есть код)
    - Удаление шума, возникшего при сканировании иероглифов (*есть код), пример ниже: 
    
    ![Bad](https://xiaoxue.iis.sinica.edu.tw/ImageText2/ShowImage.ashx?text=%ee%a3%90&font=%e4%b8%ad%e7%a0%94%e9%99%a2%e9%87%91%e6%96%87%e9%87%8d%e6%96%87%e5%85%ab&size=36&style=regular&color=%23000000 "Bad image")
    ![Good](https://xiaoxue.iis.sinica.edu.tw/ImageText2/ShowImage.ashx?text=%ee%b6%ba&font=%e4%b8%ad%e7%a0%94%e9%99%a2%e9%87%91%e6%96%87%e9%87%8d%e6%96%87%e4%b8%89&size=36&style=regular&color=%23000000 "Good image")
    - Аугментацию (*есть код)
- Модель
    - Предобученные модели ResNet34 / vgg16
    - MobileNetV3, если подразумевается создание веб-сервиса
    - Архитектура, имеющая высокий скор на MNIST датасете. Ансамбль простых сверточных сетей - [статья](https://arxiv.org/pdf/2008.10400v2.pdf)

## Возможные проблемы
- Сложность поиска достаточного объема научной литературы
- Один класс может содержать сильно непохожие друг на друга образы, например:

![One](https://xiaoxue.iis.sinica.edu.tw/ImageText2/ShowImage.ashx?text=%ee%b6%ba&font=%e4%b8%ad%e7%a0%94%e9%99%a2%e9%87%91%e6%96%87%e9%87%8d%e6%96%87%e4%b8%89&size=36&style=regular&color=%23000000 "First type")
![Two](https://xiaoxue.iis.sinica.edu.tw/ImageText2/ShowImage.ashx?text=%ee%b7%84&font=%e4%b8%ad%e7%a0%94%e9%99%a2%e9%87%91%e6%96%87%e9%87%8d%e6%96%87%e4%b8%89&size=36&style=regular&color=%23000000 "Second type")
- Высокий дисбаланс классов: >20 в одном против <2 в другом

# В ближайшее время
1. Заново соберу актуальный датасет
2. Обучу бейзлайн в fastai. Далее буду использовать только torch
