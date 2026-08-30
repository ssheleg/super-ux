# Разбор лендинга: zerorank.ai

> Форензический разбор для плейбука «как строить лендинги». Каждое
> утверждение снабжено квитанцией: дословная цитата, фрагмент HTML или
> измеренное число. Всё, что проверить не удалось, помечено «не проверено».
> Дословные цитаты сохранены в оригинале (английский).

---

## 0. Паспорт

| Поле | Значение | Квитанция |
|---|---|---|
| URL | `https://zerorank.ai/` | — |
| Дата снятия | 2026-08-30 | — |
| HTTP | `200`, редиректов нет (`url_effective = https://zerorank.ai/`) | `curl -w "%{http_code}"` |
| Вес HTML | **221 880 байт** (≈217 KB) | `curl -o /tmp/zr.html -w "%{size_download}"` → `SIZE:221880` |
| TTFB / полная загрузка HTML | 0,553 с | `curl -w "%{time_total}"` → `TIME:0.552677` |
| SSR или CSR | **SSR.** Вся продающая копия присутствует в сыром HTML | 1042 слова видимого текста извлечены из HTML без исполнения JS (`wc -w`) |
| Хостинг | Vercel | `server: Vercel`, `x-vercel-cache: HIT`, `x-vercel-id: lhr1::iad1::…` |
| Фреймворк | Next.js (App Router + React Server Components) + Payload CMS | `x-powered-by: Next.js, Payload`; в HTML — `self.__next_f.push`, `/_next/static/chunks/app/(website)/page-…js` |
| CSS | Tailwind (утилитарные классы + произвольные значения) | `class="bg-[linear-gradient(97.16deg,#161616_6.48%,#000000_94.42%)] rounded-[10px]"` |
| Шрифт | Inter | `font-inter` встречается 195 раз; два предзагруженных `.woff2` |
| Аналитика | Google Tag Manager, контейнер `GTM-NK32DVCX` | `googletagmanager.com/ns.html?id=GTM-NK32DVCX` |
| Видео | Tella (эмбед в модалке) | `https://www.tella.tv/video/vid_cmkzz005i001g04l20s537kev/embed?b=0&title=1&a=1&loop=1&t=0&muted=0&wt=0` |
| Логотипы платформ | logo.dev (сторонний CDN логотипов) | `img.logo.dev/openai.com?token=pk_fUybx3JdSg6x03wHsaWqAA&size=128&format=webp&retina=true&theme=dark` |
| A/B-тесты, session recording, чат-виджет, cookie-баннер, рекламные пиксели | **В сыром HTML не обнаружены.** Единственные внешние домены: `googletagmanager.com`, `tella.tv`, `linkedin.com`, `x.com`, `schema.org`, `w3.org` | перечень всех внешних доменов в HTML |
| Безопасность | HSTS с preload, `nosniff`, `strict-origin-when-cross-origin` | `strict-transport-security: max-age=63072000; includeSubDomains; preload` |

**Что за продукт, одним предложением.** ZeroRank — трекер видимости бренда в
ответах ИИ-поисковиков (AEO/GEO): он прогоняет ваши промпты по 17 ИИ-платформам,
показывает где, как часто и в каком тоне вас упоминают относительно конкурентов,
и выдаёт рекомендации, что править.

**ICP.** Маркетологи, агентства и SMB-команды роста. Прямые указания в копии:
`"Trusted by 1k+ marketers"`; `"For growing startups that are starting to track
and grow their AI search visibility."`; `"For agile SMEs wanting deeper insights
into their AI search efforts and faster growth."`; `"For enterprises needing
advanced tracking and custom reporting."` Агентский сегмент выдают пункты
тарифов: `"Shareable client dashboards"`, `"White-label dashboards"`,
`"Automated email reports to clients"`.

**Цена, видна на первом уровне.** Да, полный прайс на главной:

- Starter — `$76` `/month` `from` `$89`
- Pro — `$169` `/month` `from` `$199`, бейдж `"Most popular"`
- Enterprise — `Custom`

Переключатель `Monthly` / `Yearly`, подпись `"Save 15% with yearly"`. Показанные
по умолчанию $76/$169 — это **годовые** цены; месячные $89/$199 набраны
зачёркнуто-мелким как «from». (Внешнее подтверждение уровня цен: G2/AppSumo
называют старт «$76/month (yearly), regular monthly $89» — совпадает.)

---

## 1. Карта секций (по порядку)

Порядок документа, от верхней плашки до модалки. Формат:
**Название** | заголовок | подзаголовок | CTA | визуал | работа в аргументе.

---

**1. Announcement bar (плашка анонса)**

- Заголовок: бейдж `New` + `"Introducing Gap Opportunities and Fanout Query Analytics. Try it now →"`
- Подзаголовок: нет
- CTA: сама плашка — ссылка на `https://app.zerorank.ai`; продублирована сжатая мобильная версия `"Gap Opportunities & Fanout Analytics →"`
- Визуал: белая плашка во всю ширину, красный бейдж `New` — единственный светлый элемент на чёрной странице
- Работа: сигнал «продукт живой и развивается» + вброс двух терминов новой категории (`Gap Opportunities`, `Fanout Query`) до того, как посетитель увидел H1. Это же и приманка для опытного сегмента, который уже знает, что такое fanout-запросы.

---

**2. Навигация**

- Заголовок: логотип `ZeroRank`
- Пункты: `Pricing` · `Clients` · `Wall of Love` · `Blog` · `About` · `Contact`
- CTA: `Log In` (текстом) + `Start Free Trial` (оранжевая кнопка)
- Визуал: тёмная прозрачная шапка, липкая при скролле (подтверждено скриншотами: шапка на месте на всех позициях скролла)
- Работа: два отдельных пункта под соцдоказательство (`Clients` и `Wall of Love`) — редкое решение: доверие вынесено в навигацию первого уровня, а не спрятано в футер. Единственная конверсионная кнопка одна и та же на всех экранах.

---

**3. Hero**

- Бейдж над заголовком: `"Trusted by 1k+ marketers"` (со звёздочкой)
- Заголовок (H1, видимая часть): `"Rank #1 in"` + **вращающееся** имя платформы с её логотипом — на момент снятия `ChatGPT`
- Заголовок (H1, машиночитаемая часть, `sr-only`): `"Rank #1 in ChatGPT, Perplexity, Gemini, Google AI Mode, Google AI Overviews, Grok, Bing Copilot, Claude, DeepSeek"`
- Подзаголовок: `"Track and improve your visibility across AI platforms. Reach customers before your competitors do."`
- CTA: **форма**, а не кнопка — `<input placeholder="your-website.com" name="url" autoComplete="url">` + кнопка `Analyze`
- Микрокопия под CTA: `"Setup in 2 mins"` · `"No credit card required"`
- Визуал: чёрный фон, точечная сетка с оранжевыми искрами (`/hero-background.svg`), оранжевое свечение вокруг поля ввода, крупный жирный Inter (72px на desktop)
- Работа: **самая нагруженная секция страницы.** Обещание («быть №1»), место действия (9 названных платформ), метод (введи домен — получи анализ), и снятие двух главных возражений (время, карта) — всё в одном экране. Форма вместо кнопки превращает «зарегистрируйся» в «посмотри на себя», то есть переносит первый шаг с обязательства на любопытство.

---

**4. Скриншот продукта (hero-визуал)**

- Заголовок / подзаголовок / CTA: нет
- Визуал: `/dashboard-preview.webp`, `alt="ZeroRank Dashboard - AI visibility tracking and brand monitoring"`, предзагружается с `fetchPriority="high"`
- **Дефект, измерен.** В браузере (Chrome, десктоп 1568×780) на этом месте — **пустой чёрный прямоугольник примерно в высоту экрана**. Воспроизведено дважды, на двух независимых загрузках страницы, на нескольких позициях скролла. При этом сам файл доступен: `HTTP 200`, 314 700 байт, `RIFF … Web/P image, VP8, 5192x3132`. То есть это не 404, а не сработавший клиентский reveal (или неуспевшее декодирование картинки 5192 px шириной). Работу «показать продукт» секция в момент замера не выполняла.
- Работа (по замыслу): доказательство существования продукта сразу после обещания.

---

**5. Логотипная плашка**

- Заголовок: `"Trusted by teams at:"`
- CTA: нет
- Визуал: 5 белых монохромных логотипов — `The Optimizer`, `AdPlexity`, `ClickFlare`, `STM`, `LanderLab` (локальные SVG в `/logos/`, у каждого осмысленный `alt`)
- Работа: соцдоказательство. Все пять — из одной ниши (affiliate/performance-маркетинг, трекеры и форумы), то есть плашка адресована конкретному племени, а не «всем». Слабость: это же и потолок — ни одного узнаваемого за пределами ниши бренда.

---

**6. Features**

- Надзаголовок: `Features` (оранжевый, с иконкой-молнией)
- Заголовок (H2): `"Everything You Need to Win in AI Search"`
- Подзаголовок: `"Track where your brand appears, why it doesn't, and what to improve next."`
- CTA: `Start Free Trial` (справа от заголовка, на одной строке)
- Карточки (4):
  1. `"Discover the Prompts That Matter"` — `"Find the AI questions where your brand should appear — backed by real query data and AI search volumes — and spot new opportunities before your competitors."`
  2. `"Track Your AI Rankings"` — `"See where your brand appears across 17 AI platforms — ChatGPT, Perplexity, Gemini, Google AI Overviews, Claude, and more — updated daily with in-depth analytics."`
  3. `"Analyze Sentiment & Visibility"` — `"See how AI is talking about your brand: monitor tone, how often you're mentioned, and your ranking - all in one dashboard."`
  4. `"Outrank Your Competitors"` — `"Benchmark your brand's visibility, ranking and mentions — and get notified when you're slipping behind or gaining the lead."`
- Визуал: сетка 2×2, у каждой карточки — свой SVG-макет интерфейса (чипы промптов, столбчатая диаграмма `58% / 41% / 29%` с логотипами моделей). Подтверждено скриншотом.
- Работа: механизм. Отвечает «что именно оно делает», разложив на четыре глагола: найти промпты → отследить позиции → разобрать тональность → сравнить с конкурентами.

---

**7. Benefits**

- Надзаголовок: `Benefits`
- Заголовок (H2): `"Turn AI Visibility Into Customer Growth"`
- Подзаголовок: `"Show up when customers ask AI who to trust and stay ahead of competitors."`
- CTA: `Start Free Trial`
- Пункты (4, H3 + строка):
  1. `"Win More AI Recommendations"` — `"Be the brand AI chooses when buyers compare options."`
  2. `"Move Before Competitors Do"` — `"Spot prompt trends, citation shifts, and ranking changes early."`
  3. `"Turn Insights Into Action"` — `"Know exactly what to fix next across content, authority, and technical signals."`
  4. `"Strengthen Your Brand Authority"` — `"Build the signals AI relies on when recommending brands."`
- Визуал: `/product-features.webp` (`alt="ZeroRank AI Dashboard"`) + 4 иконки
- Работа: перевод функций в исходы. Ровно та же четвёрка, что в Features, но на языке результата — приём «одна механика, два пересказа»: сначала для скептика (что делает), потом для покупателя (что мне с этого).

---

**8. How It Works**

- Надзаголовок: `How It Works`
- Заголовок (H2): `"Get Started in Minutes"`
- Подзаголовок: `"Three simple steps to understand and improve your AI search visibility."`
- CTA: `Start Free Trial`
- Шаги:
  1. `"1 - Add Your Brand"` — `"Enter your brand name, website, and competitors."`
  2. `"2 - Track & Analyze"` — `"See live visibility, position, sentiment and competitor benchmarking across AI models."`
  3. `"3 - Optimize & Win"` — `"Leverage insights to publish, optimize and outrank your competitors in AI-search results."`
- Визуал: 3 SVG-иллюстрации (`/hiw-add-brand.svg`, `/hiw-track-analyze.svg`, `/hiw-optimize-win.svg`)
- Работа: снятие риска через снижение воспринимаемых трудозатрат. Шаг 1 — единственный, который требует чего-то от пользователя, и он описан тремя существительными: имя, сайт, конкуренты. Перекликается с микрокопией героя `"Setup in 2 mins"`.

---

**9. Testimonials**

- Надзаголовок: `Testimonials`
- Заголовок (H2): `"Trusted by Teams Winning in AI Search"`
- Подзаголовок: `"See how top teams use ZeroRank AI to win AI search."`
- CTA: `Start Free Trial`
- Отзывы (3), каждый — крупная метрика + заголовок-цитата + развёрнутая цитата + фото + имя + должность:
  1. `3x` / `mention growth` — `"ZeroRank changed how we approach AI search."` / `"We realized we were missing from a large share of relevant AI answers. Within two months, our mentions grew 3x."` — **Ervis Bregasi, CEO, ClickFlare**
  2. `225%+` / `visibility improvement` — `"We went from manually checking prompts for hours to having everything in one place."` / `"Visibility improved by over 225%."` — **Guido Silbert, Marketing & Growth, AdPlexity**
  3. `4.6x` / `AI visibility increase` — `"AI is becoming a real acquisition channel for us."` / `"With ZeroRank, our AI visibility increased 4.6x and we're seeing more users come in already knowing what we do and why they want us."` — **Ervin Hoxha, CEO, LanderLab**
- Визуал: фото людей (`/testimonials/ervis.webp` и т. д.), иконка кавычек
- Работа: доказательство результата. Три компании из отзывов — три из пяти логотипов плашки выше (`ClickFlare`, `AdPlexity`, `LanderLab`), то есть логотип и цитата подкрепляют друг друга, а не живут порознь.

---

**10. Pricing**

- Надзаголовок: `Pricing`
- Заголовок (H2): `"Our Pricing"`
- Подзаголовок: `"Track and improve your AI search visibility with clear analytics and actionable recommendations."`
- Управление: `Monthly` / `Yearly` + `"Save 15% with yearly"`
- CTA: `Start for Free` (×2) и `Request Demo` (Enterprise, ведёт на `/book-demo`)
- Тарифы: см. паспорт. Различающиеся строки — только объём:
  `4,500` / `13,500` / `31,500+` `AI answers analyzed per month`;
  `15` / `50` / `150` `Prompt Research runs per month`;
  `3` / `12` / `36` `AI article generations + … content optimizations per month`;
  поддержка `Email + Live Chat` → `Email, Live Chat + Slack Support`.
  Всё остальное — **одинаково на всех тарифах**, включая `"Unlimited prompts & AI models"`, `"MCP server + REST API access"`, `"Unlimited countries & seats"`, `"White-label dashboards"`, `"Single sign-on (SSO)"`, `"Dedicated Account Rep"`.
- Работа: снятие ценового риска и позиционирование против конкурентов, которые берут за место и за страну. `"Unlimited countries & seats"` на самом дешёвом тарифе — это выпад в сторону агентств, у которых у конкурентов растёт счёт от числа клиентов.
- Замечание: списки визуально одинаковы у всех трёх тарифов, различия зашиты только в числах внутри строк. Понять, чем Starter отличается от Pro, можно лишь сравнивая цифры глазами — таблицы сравнения нет.

---

**11. FAQ**

- Надзаголовок: `FAQ's` (грамматическая ошибка: апостроф во множественном числе)
- Заголовок (H2): `"Questions? We've Got Answers."`
- Подзаголовок: `"Here are answers to the most common things people ask before getting started."`
- CTA: `Contact Support` → `/contact`
- Вопросы (6, аккордеон):
  1. `"How do you track AI search visibility?"` → **ответ в HTML есть**: `"We run your prompts across the AI platforms you enable — as often as daily — and monitor mentions, positions, citations and sentiment in one dashboard."`
  2. `"Do I need technical skills to use ZeroRank AI?"` → ответа в HTML **нет**
  3. `"Which AI platforms are supported?"` → ответа в HTML **нет**
  4. `"Can I compare against competitors?"` → ответа в HTML **нет**
  5. `"Is my data secure?"` → ответа в HTML **нет**
  6. `"Is there a free trial?"` → ответа в HTML **нет**
- Квитанция: разметка закрытых пунктов — `<button … aria-expanded="false"><span>Do I need technical skills to use ZeroRank AI?</span>…</button>` и сразу закрывающий `</div>`; текста ответа между ними нет. Независимо подтверждено WebFetch, который вернул `[Answer not visible in provided content]` по пяти из шести вопросов.
- Работа: снятие возражений — но выполняется только для человека, который кликнет. Подробности в разделе 8.

---

**12. Финальный CTA**

- Заголовок (H2): `"Ready to win more customers through AI search?"`
- Подзаголовок: `"Start your free trial and see where AI recommends your brand and what to improve next."`
- CTA: `Start Free Trial`
- Визуал: `/final-cta-models.svg` (`alt="AI Models"`)
- Работа: последний сбор. Формулировка переносит фокус с продукта (видимость) на деньги (клиенты) — «more customers», а не «more visibility».

---

**13. Футер**

- Строка миссии: `"AI search is changing how people discover brands. ZeroRank AI helps you act before your competitors do."`
- Бейджи доверия: `"Secure and compliant"` · `"99.9% uptime"` (с иконками)
- Копирайт: `"© 2026 ZeroRank. All rights reserved."`
- Три колонки (H5):
  - `Sections`: Features, Pricing, FAQ, Testimonials, Benefits, Refund Policy
  - `Socials`: Twitter/X, Linkedin
  - `Pages`: Home, About, Brand Ambassador, Blog, Clients, Wall of Love, Contact, Free Tools, Comparisons, Book a Demo
- CTA: `Start for free` → `https://app.zerorank.ai/signup`
- Работа: главный распределитель внутренних ссылок. Именно здесь (и только здесь) видны `Free Tools` и `Comparisons` — два самых массивных SEO-актива сайта.

---

**14. Плавающий видео-виджет (фиксированный, правый нижний угол)**

- Заголовок (H3): `"See ZeroRank in action"`
- Подзаголовок: `"Watch a 2-minute demo"`
- CTA: сама карточка, открывает модалку
- Визуал: миниатюра `/video-thumbnail.webp` с кнопкой play; присутствует на всех позициях скролла (подтверждено тремя скриншотами)
- Работа: постоянно доступный «низкообязательный» путь для тех, кто не готов вводить домен. Единственный элемент страницы, который не уезжает при скролле, кроме шапки.

---

**15. Видео-модалка + встроенный в неё CTA**

- Видео: iframe Tella (`vid_cmkzz005i001g04l20s537kev`), 16:9, `allow="autoplay; fullscreen"`
- Под видео, в той же модалке:
  - Заголовок (H3): `"Ready to dominate AI search?"`
  - Подзаголовок: `"Join 1000+ brands already tracking their AI visibility."`
  - Галочки: `"7-day free trial"` · `"Cancel anytime"`
  - CTA: `Start for free`
  - Микрокопия: `"Setup takes less than 2 minutes"`
- Разметка в DOM всегда, скрыта через `class="fixed inset-0 z-70 … opacity-0 pointer-events-none"`
- Работа: **лучший приём страницы.** Конверсионный блок приклеен к концу демо — обращается к самому прогретому человеку на сайте, тому, кто только что посмотрел двухминутное видео. Обратите внимание: `"7-day free trial"` — конкретный срок — сказан **только здесь** и нигде больше на странице.

---

## 2. Продающий аргумент

**Оффер.** Бесплатный триал SaaS-подписки за $76–169/мес, вход без карты:
`"No credit card required"`, `"Setup in 2 mins"`. Первый шаг — не регистрация,
а анализ своего домена: `placeholder="your-website.com"` + кнопка `Analyze`.

**Обещание / результат.** Заявлено на трёх уровнях крупности:

1. Максимальное, в H1: `"Rank #1 in ChatGPT, Perplexity, Gemini…"` — обещание
   позиции.
2. Среднее, в подзаголовке: `"Track and improve your visibility across AI
   platforms. Reach customers before your competitors do."` — обещание
   видимости и опережения.
3. Денежное, в финальном CTA: `"Ready to win more customers through AI
   search?"` — обещание клиентов.

Лестница честная: чем ближе к кнопке, тем ближе к деньгам.

**Механизм.** Назван и разложен, а не спрятан за «AI-powered». Самая полная
формулировка — в единственном раскрытом FAQ: `"We run your prompts across the
AI platforms you enable — as often as daily — and monitor mentions, positions,
citations and sentiment in one dashboard."` Дополняется четырьмя карточками
Features и тремя шагами How It Works. Четыре измеряемые сущности названы прямым
текстом: `mentions, positions, citations and sentiment`.

**Доказательства.** Четыре слоя, идущие по нарастанию проверяемости:

- Счётчик: `"Trusted by 1k+ marketers"` (герой), `"Join 1000+ brands"` (модалка)
- Логотипы: 5 названных компаний
- Именованные отзывы с числами: `3x`, `225%+`, `4.6x` — с именем, должностью,
  компанией и фото
- Скриншоты интерфейса в карточках Features (диаграмма `58% / 41% / 29%`)

**Снятие риска.** Плотно и в правильных местах:
`"No credit card required"` (под первым CTA), `"Setup in 2 mins"` (там же),
`"7-day free trial"` + `"Cancel anytime"` (в модалке),
`"Start for Free"` на платных тарифах, `Refund Policy` в футере,
`"Secure and compliant"` + `"99.9% uptime"` в футере, `"Is my data secure?"` в FAQ.

**Срочность.** Не дедлайновая, а конкурентная — единственный вид срочности на
странице, и он проведён сквозь весь текст:
`"Reach customers before your competitors do."` · `"spot new opportunities
before your competitors"` · `"Move Before Competitors Do"` · `"get notified when
you're slipping behind"` · `"ZeroRank AI helps you act before your competitors
do."` Ни одного таймера, ни одного «предложение действует до».

**Враг.** Двойной, и это осознанное решение:

1. *Внешний враг* — конкурент, которого ИИ рекомендует вместо вас. Он назван
   пять раз (выше) и он же — источник срочности.
2. *Внутренний враг* — ручная работа. `"We went from manually checking prompts
   for hours to having everything in one place."` Это враг из отзыва, а не из
   копирайта, — приём сильнее, потому что о боли говорит покупатель.

Третий, невысказанный враг — незнание: `"We realized we were missing from a
large share of relevant AI answers."` Страх «я не знаю, что происходит»
проговаривается только чужим голосом.

---

## 3. Позиционирование и месседжинг

**Категория.** «AI search visibility» — так она названа в title, в мета-описании
и в H2 секций. Слова `AEO` и `GEO` на главной **отсутствуют** (проверено: 0
вхождений), хотя в блоге под них есть отдельные статьи (`/blog/aeo-vs-seo`,
`/blog/geo-vs-aeo`, `/blog/geo-strategy`). Решение осознанное: главная говорит
описательно, аббревиатуры оставлены тем, кто уже ищет по ним.

**Альтернатива, от которой отстраиваются.** Названа только в отзыве —
ручная проверка промптов (`"manually checking prompts for hours"`). На главной
нет ни одного упоминания конкурента по имени. Вся конкурентная работа вынесена
на отдельные страницы `/vs/*` (6 штук: `ahrefs-brand-radar`, `promptwatch`,
`scrunch-ai`, `airops`, `peec-ai`, `profound-ai`).

**Before / after.**

| Before | After |
|---|---|
| «Мы не знали, что нас нет в ответах» (`"We realized we were missing from a large share of relevant AI answers."`) | `"Be the brand AI chooses when buyers compare options."` |
| «Часы ручной проверки» (`"manually checking prompts for hours"`) | `"having everything in one place"` |
| «ИИ рекомендует конкурента» | `"Rank #1 in ChatGPT…"` |

**Адресат.** Маркетолог/агентство/SMB — прямо назван (см. паспорт).

**Уровень осведомлённости на первом экране.** По Шварцу — **problem-aware,
переходящий в solution-aware**, но НЕ product-aware. Разбор:

- H1 не объясняет, что такое видимость в ИИ-поиске, — он предполагает, что вы
  уже знаете, что ИИ вас где-то упоминает или не упоминает. Это problem-aware.
- H1 при этом перечисляет **девять платформ поимённо** — тем самым доопределяя
  проблему для того, кто её не осознал: «вот девять мест, где вас могут не быть».
  Это дешёвый способ дотянуть unaware до problem-aware, не тратя на объяснение
  отдельный экран.
- Форма `your-website.com` + `Analyze` работает на все уровни сразу: она не
  требует понимания продукта, только любопытства к себе.

**Как продаётся новая, ещё не осознанная категория — через страх, новизну или
данные?** Измеримо: **через страх конкурентной потери, поданный языком данных, а
не языком паники.**

- *Страх* — да, но специфический. Не «ИИ убьёт ваш трафик», не «SEO мертво». Ни
  одного апокалиптического утверждения на странице нет. Страх ровно один и
  всегда относительный: конкурент опередит. `"Reach customers before your
  competitors do."` Это страх отставания, а не гибели, — он не требует от
  читателя принять мрачную картину мира, только допустить, что кто-то шустрее.
- *Новизна* — используется как крючок, а не как аргумент. Плашка `New` вверху,
  термины `Gap Opportunities`, `Fanout Query Analytics`; в футере одна
  декларативная строка о смене эпохи: `"AI search is changing how people
  discover brands."` Одна строка на всю страницу — новизна намеренно не педалится.
- *Данные* — главный носитель. Категория делается реальной через её измеримость:
  `17 AI platforms`, `4,500 / 13,500 / 31,500+ AI answers analyzed per month`,
  `mentions, positions, citations and sentiment`, диаграмма `58% / 41% / 29%`,
  результаты `3x`, `225%+`, `4.6x`. Это ключевой ход: **новую категорию
  легитимизируют не объяснением, а метрикой.** Если у явления есть единица
  измерения, тариф и дашборд, оно перестаёт быть гипотезой.

Механику стоит запомнить целиком: **назвать площадки поимённо (существование) →
дать метрику (измеримость) → показать конкурента, который уже там (срочность) →
предложить бесплатно посмотреть на себя (проверка).** Ни на одном шаге у
читателя не просят поверить в тезис о будущем.

---

## 4. Копирайтинг: конкретные приёмы

### Формула H1

Дословно, видимая часть: `Rank #1 in` + `[ChatGPT | Perplexity | Gemini | Google
AI Mode | Google AI Overviews | Grok | Bing Copilot | Claude | DeepSeek]`.

Дословно, `sr-only`-часть: `"Rank #1 in ChatGPT, Perplexity, Gemini, Google AI
Mode, Google AI Overviews, Grok, Bing Copilot, Claude, DeepSeek"` (113 знаков).

Разбор:

- **Глагол в императиве + превосходная позиция + конкретное место.** `Rank` —
  глагол, знакомый каждому SEO-специалисту, перенесённый в новый контекст. `#1`
  — числовой абсолют, не требующий пояснения. `in ChatGPT` — место, которое до
  2023 года не существовало как площадка ранжирования.
- **Заимствование ментальной модели.** «Ранжироваться №1» — готовая, полностью
  освоенная концепция из SEO. Новая категория продаётся **не как новая**: её
  подают как старую задачу на новой территории. Это дешевле, чем объяснять
  категорию с нуля.
- **Вращение как способ вместить длинный список.** Человек читает короткое
  «Rank #1 in ChatGPT»; краулер и скринридер получают все девять названий.
  Реализация: `<span class="sr-only">…все девять…</span>` +
  `<span aria-hidden="true">Rank #1 in</span>` + `<span aria-live="polite"
  aria-atomic="true">` с текущей платформой. Приём разобран отдельно в разделе 10.
- **Чего в H1 нет:** названия продукта, слова «AI-powered», слова «platform»,
  «solution», «tool». Ни одного существительного-категории.

### Длина заголовков

| Заголовок | Знаков | Слов |
|---|---|---|
| H1 видимый (`Rank #1 in ChatGPT`) | 18 | 4 |
| H1 `sr-only` | 113 | 16 |
| `Everything You Need to Win in AI Search` | 39 | 8 |
| `Turn AI Visibility Into Customer Growth` | 39 | 6 |
| `Get Started in Minutes` | 22 | 4 |
| `Trusted by Teams Winning in AI Search` | 37 | 6 |
| `Our Pricing` | 11 | 2 |
| `Questions? We've Got Answers.` | 29 | 4 |
| `Ready to win more customers through AI search?` | 45 | 8 |
| `<title>` | 52 | — |
| `<meta description>` | 98 | — |

Медиана H2 — **37 знаков / 6 слов.** Ни один заголовок страницы не длиннее 45
знаков. Это жёсткая и выдержанная норма.

### Субъект предложений

Подавляющее большинство — **второе лицо, «вы» в роли деятеля**, глагол в
повелительном или изъявительном наклонении с опущенным подлежащим:
`"Track where your brand appears…"`, `"Find the AI questions where your brand
should appear…"`, `"See where your brand appears across 17 AI platforms…"`,
`"Know exactly what to fix next…"`, `"Be the brand AI chooses…"`,
`"Enter your brand name, website, and competitors."`

Продукт как подлежащее появляется ровно дважды и оба раза — в служебных местах:
`"ZeroRank AI helps you act before your competitors do."` (футер) и `"We run
your prompts across the AI platforms you enable…"` (FAQ). То есть **страница
почти нигде не говорит «мы делаем» — она говорит «вы делаете».**

Третий субъект, и он тут особенный: **ИИ как действующее лицо.** `"Be the brand
AI chooses when buyers compare options."` · `"See how AI is talking about your
brand"` · `"Build the signals AI relies on when recommending brands."` ·
`"see where AI recommends your brand"`. ИИ подан как субъект с предпочтениями —
не инструмент, а привратник, которого нужно расположить к себе. Это и есть
риторический фундамент всей категории.

### Три самые конкретные формулировки (дословно)

1. `"We run your prompts across the AI platforms you enable — as often as daily
   — and monitor mentions, positions, citations and sentiment in one
   dashboard."` — механизм, частота и четыре именованные метрики в одном
   предложении. Проверяемо целиком.
2. `"See where your brand appears across 17 AI platforms — ChatGPT, Perplexity,
   Gemini, Google AI Overviews, Claude, and more — updated daily with in-depth
   analytics."` — число + примеры + частота обновления.
3. `"Enter your brand name, website, and competitors."` — три существительных,
   исчерпывающее описание работы пользователя. Самая честная строка на странице:
   она обещает мало и потому ей веришь.

Почётное упоминание — прайс: `"Up to 4,500 AI answers analyzed per month"`,
`"15 Prompt Research runs per month"`. Единица тарификации названа прямо
(«проанализированный ответ ИИ»), что в этой категории редкость.

### Три самые пустые формулировки (дословно)

1. `"Everything You Need to Win in AI Search"` — «всё, что нужно» не сообщает
   ничего и не может быть ложным. Классический заполнитель заголовка секции.
2. `"Turn Insights Into Action"` — существительное «инсайты» плюс существительное
   «действие» без единой детали. Подстрочник спасает
   (`"Know exactly what to fix next across content, authority, and technical
   signals."`), но сам заголовок пуст.
3. `"Leverage insights to publish, optimize and outrank your competitors in
   AI-search results."` — `Leverage insights` в начале шага «как это работает»
   ровно там, где читатель ждёт конкретики. Шаги 1 и 2 конкретны, шаг 3 —
   абстракция; это же и самое слабое место воронки, потому что именно третий шаг
   и есть обещанный результат.

Рядом: `"Strengthen Your Brand Authority"` / `"Build the signals AI relies on
when recommending brands."` — какие сигналы, не сказано ни здесь, ни где-либо
на странице.

### Числа

Все числа страницы, по типу:

- **Масштаб пользовательской базы:** `1k+ marketers`, `1000+ brands` — одно и то
  же число в двух записях и с двумя разными существительными («маркетологи» и
  «бренды»). Нестыковка; см. раздел 9.
- **Охват:** `17 AI platforms` (5 раз), 9 платформ поимённо в H1
- **Скорость:** `Setup in 2 mins`, `Setup takes less than 2 minutes`,
  `2-minute demo`, `Get Started in Minutes`, `daily`
- **Результат клиента:** `3x`, `225%+`, `4.6x`, `Within two months`
- **Цена:** `$76`, `$89`, `$169`, `$199`, `Save 15%`, `Custom`
- **Ёмкость тарифа:** `4,500` / `13,500` / `31,500+`, `15` / `50` / `150`,
  `3` / `12` / `36`
- **Доверие:** `99.9% uptime`, `7-day free trial`
- **Продуктовые:** `58% / 41% / 29%` (на SVG-диаграмме карточки)
- **Структура:** `Three simple steps`, `1 -`, `2 -`, `3 -`

Всего свыше 30 числовых утверждений на 1042 слова — примерно одно число на 35
слов. Это плотность технического документа, не рекламной страницы, и она —
главный носитель убедительности (см. раздел 3).

### Глаголы

Ядро — глаголы победы и опережения: `Rank`, `Win` (6 раз), `Outrank`,
`Dominate`, `Beat` (через `outrank`), `Move Before`, `Reach … before`, `Join`.
Рабочий слой: `Track` (7), `Improve` (4), `Analyze` (3), `Monitor` (2),
`Benchmark`, `Spot`, `Discover`, `Find`, `See` (6), `Know`, `Build`,
`Strengthen`, `Turn`, `Enter`, `Add`, `Optimize`, `Publish`, `Leverage`.

Ни одного пассивного залога в заголовках. Ни одного модального «can», «could»,
«might» во всей странице — обещания заявлены в изъявительном наклонении.

### Все надписи кнопок и конверсионных ссылок (дословно)

| Надпись | Раз | Куда ведёт |
|---|---|---|
| `Start Free Trial` | 7 | `https://app.zerorank.ai` |
| `Start for Free` | 2 | `https://app.zerorank.ai` |
| `Start for free` | 1 | `https://app.zerorank.ai/signup` |
| `Log In` | 2 | `https://app.zerorank.ai` |
| `Analyze` | 1 | форма героя |
| `Request Demo` | 1 | `/book-demo` |
| `Book a Demo` | 1 | `/book-demo` |
| `Contact Support` | 1 | `/contact` |
| `Try it now →` / `Gap Opportunities & Fanout Analytics →` | 1 | `https://app.zerorank.ai` |

**15 конверсионных ссылок, 6 уникальных надписей** для одного и того же
действия. `Start Free Trial` / `Start for Free` / `Start for free` — три записи
одного действия; `Request Demo` / `Book a Demo` — две записи другого. См.
раздел 9.

### Микрокопия под CTA

- Под формой героя: `"Setup in 2 mins"` · `"No credit card required"`
- В модалке: `"7-day free trial"` · `"Cancel anytime"` · `"Setup takes less
  than 2 minutes"`
- В футере: `"Secure and compliant"` · `"99.9% uptime"`
- Над H1: `"Trusted by 1k+ marketers"`

Правило, которое здесь выдержано: **у каждой конверсионной точки первого экрана
есть строка снятия возражения непосредственно под ней.** Возражения выбраны
разные и не повторяются: время (2 мин), деньги (без карты), обязательство
(отмена в любой момент), безопасность (compliant), надёжность (99.9%).

### Тон

Уверенный, соревновательный, безличный к себе и предельно личный к читателю.
Регистр — деловой английский без жаргона; из терминов категории на главной
только `AI search visibility`, `prompts`, `citations`, `sentiment`, `fanout`.
Ни одного восклицательного знака. Ни одного эмодзи. Ни одной шутки. Ни одного
«just», «simply», «effortlessly». Обращение — исключительно на «вы».

### Признаки машинной генерации

Что **указывает** на LLM-черновик:

- **Риторическое тире, 13 вхождений**, часть — в роли запятой или двоеточия:
  `"Find the AI questions where your brand should appear — backed by real query
  data and AI search volumes — and spot new opportunities…"`,
  `"Daily tracking — or weekly, monthly, and on-demand runs"`. Это самый громкий
  маркер машинного черновика в тексте.
- **Идеально параллельные четвёрки.** Features и Benefits — по 4 пункта,
  заголовок каждого — «глагол + объект» из 3–4 слов, подпись — одно предложение
  на 8–14 слов. Ритм не сбивается ни разу; живой текст обычно сбивается.
- **Title Case на всех заголовках** без исключений.
- `"Everything You Need to Win in AI Search"` — узнаваемая LLM-заготовка
  заголовка секции возможностей.
- **Пустая абстракция ровно там, где кончился фактический материал:**
  `"Turn Insights Into Action"`, `"Strengthen Your Brand Authority"`.

Что **указывает на человеческую правку** (и это важнее для нашего плейбука):

- Непоследовательная типографика — признак ручного редактирования поверх:
  тире-дефис вместо длинного тире в одном месте (`"…and your ranking - all in
  one dashboard."`) при 13 длинных тире в остальных; шаги пронумерованы
  дефисом (`"1 - Add Your Brand"`), а не длинным тире.
- Смешанные апострофы: 1 типографский (`"why it doesn’t"`) против 6 прямых
  (`"you're"`, `"We've"`, `"brand's"`, `"FAQ's"`).
- `"FAQ's"` — грамматическая ошибка (апостроф во множественном числе), которую
  LLM почти не делает, а человек делает часто.
- Отзывы написаны неровно и с оговорками — `"a large share of relevant AI
  answers"` вместо круглого числа; это звучит как расшифровка реального разговора.

**Вывод по разделу:** каркас похож на LLM-черновик, поверх которого прошлись
руками, но прошлись не везде. Правило для нашего скила: *непоследовательность
типографики — более надёжный детектор ручной правки, чем наличие тире.*

---

## 5. Доказательства и доверие

| Элемент | Что именно | Проверяемо? |
|---|---|---|
| Логотипы | `The Optimizer`, `AdPlexity`, `ClickFlare`, `STM`, `LanderLab` — локальные SVG с осмысленным `alt` | **Частично.** Компании реальны и существуют; что они платящие клиенты — со страницы не следует. Косвенное подтверждение: три из пяти дали именные отзывы. |
| Отзывы | 3 штуки, каждый — имя + должность + компания + фото | **Да, атрибутированы полностью.** `Ervis Bregasi, CEO, ClickFlare`; `Guido Silbert, Marketing & Growth, AdPlexity`; `Ervin Hoxha, CEO, LanderLab`. Проверяемы по LinkedIn (не проверял). Ни у одного нет ссылки на профиль — это стоило бы добавить. |
| Числа результата | `3x mention growth`, `225%+ visibility improvement`, `4.6x AI visibility increase` | **Нет.** Источник — только слова клиента. Методика («что считается visibility», база отсчёта, период) не раскрыта нигде на странице. `"Within two months"` — единственная временная рамка из трёх. |
| `Trusted by 1k+ marketers` | Бейдж над H1 | **Нет.** Ни ссылки, ни даты, ни определения. В модалке то же число дано как `"Join 1000+ brands"` — маркетологи и бренды это разные единицы. |
| `99.9% uptime` | Бейдж футера | **Нет.** Нет status-страницы, нет SLA-ссылки. Декоративно. |
| `Secure and compliant` | Бейдж футера | **Нет.** Не назван ни один стандарт (SOC 2, GDPR, ISO). Формулировка максимально общая — самый декоративный элемент доверия на странице. |
| Скриншоты продукта | Карточки Features содержат нарисованные SVG-макеты интерфейса (чипы промптов, диаграмма `58% / 41% / 29%`) | **Иллюстрации, не скриншоты.** Числа на диаграмме — оформительские. |
| Главный скриншот | `/dashboard-preview.webp`, 5192×3132 | **Файл реален (314 700 байт), но в браузере на его месте пусто** — см. секцию 4 карты. |
| Демо-видео | Tella, 2 минуты, в модалке | **Да** — единственное настоящее доказательство существования интерфейса, доступное посетителю в момент замера. Содержимое не смотрел. |
| Кейсы | На главной нет. В блоге есть `/blog/ai-search-optimization-case-study`, `/blog/ai-search-visibility-case-study`, категория `/blog/category/case-studies` | Не проверено (содержимое не читал) |
| Бейджи площадок (G2, Product Hunt, AppSumo) | **Отсутствуют на странице.** При этом внешне ZeroRank присутствует на G2 и AppSumo (рейтинг 4.9 при 39 отзывах — по данным поиска, не со страницы) | Пропущенная возможность: чужой рейтинг проверяем, а `1k+ marketers` — нет |
| Отдельные страницы доверия | `/clients`, `/wall-of-love` — вынесены в главное меню | Не проверено (не открывал) |

**Итог по разделу.** Верхний слой доверия (люди, компании, отзывы) —
атрибутирован и добротен. Нижний (числа результата, размер базы, безопасность,
аптайм) — целиком декоративен: ни одно из этих чисел не имеет источника,
методики или ссылки. Для продукта, который продаёт **измерение**, это
диссонанс, и его стоит записать в плейбук как отдельный риск:
*продавая метрику, свои собственные метрики нужно подкреплять строже обычного.*

---

## 6. Механика конверсии

**Количество CTA.** 15 конверсионных ссылок в HTML (без учёта навигационных
якорей футера). Из них 12 ведут на `app.zerorank.ai` (регистрация/вход), 2 — на
`/book-demo`, 1 — на `/contact`.

**Уникальных надписей — 6** для двух действий (см. таблицу в разделе 4).

**Первый CTA над сгибом?** Да, и их два: кнопка `Start Free Trial` в шапке и
форма `your-website.com` + `Analyze` в центре героя. Оба видны без скролла
(подтверждено скриншотом 1568×780).

**Один путь или несколько.** Три, с явной иерархией по «температуре»:

1. **Горячий, основной** — форма героя `Analyze` → анализ своего домена.
   Единственный путь, дающий ценность до регистрации.
2. **Тёплый, повторяющийся** — `Start Free Trial` × 7. Одна и та же оранжевая
   кнопка в конце каждой секции; ритм «аргумент → кнопка», пять раз подряд.
3. **Холодный / крупный чек** — `Request Demo` и `Book a Demo` → `/book-demo`.
   Только в тарифе Enterprise и в футере, нигде выше.

Плюс два вспомогательных: `Contact Support` (FAQ) и видео-виджет.

**Форма и поля.** Одно поле: `<input type="text" name="url"
placeholder="your-website.com" autoComplete="url">`. Ни email, ни имени, ни
пароля. Кнопка `Analyze`. Это минимально возможное трение для входа.

**Трение.** Замерено по тому, что страница обещает:

- До первого результата: 1 поле, 0 обязательств (`"No credit card required"`)
- До аккаунта: `"Setup in 2 mins"` / `"Setup takes less than 2 minutes"`
- Обратный выход: `"Cancel anytime"`
- Что происходит после `Analyze` — **не проверено** (форму не отправлял;
  вероятнее всего, домен переносится в регистрацию на `app.zerorank.ai`, но
  доказательства этому на странице нет).

**Цены.** Полный прайс на главной, три тарифа, переключатель `Monthly`/`Yearly`
с `"Save 15% with yearly"`, `"Most popular"` на среднем. По умолчанию показан
годовой (дешёвый) вариант — распространённый приём, но здесь смягчён тем, что
месячная цена тут же видна как `from $89`. Отдельная страница `/pricing`
дублирует блок и добавляет 8 вопросов FAQ.

**Вторичные пути.** `Clients` и `Wall of Love` в главном меню (соцдоказательство
как отдельный раздел сайта), `Free Tools` и `Comparisons` в футере, `Blog`,
`Book a Demo`, `Contact`.

**Sticky.** Липкая шапка с кнопкой (подтверждено на всех позициях скролла) +
фиксированный видео-виджет в правом нижнем углу. Липкой нижней панели с CTA нет.

**Exit-intent.** **Не обнаружен.** Блок, который выглядит как exit-intent
(`"Ready to dominate AI search?"`), на деле находится внутри видео-модалки, под
плеером: `class="fixed inset-0 z-70 … opacity-0 pointer-events-none"` →
iframe Tella → и уже под ним заголовок и CTA. Триггер — клик по видео-виджету,
а не намерение уйти.

**Чат.** Живого чат-виджета в HTML нет (Intercom, Crisp, Drift и т. п. не
найдены). При этом `"Email + Live Chat Support"` заявлен во всех тарифах — то
есть чат существует в продукте, но не на лендинге.

**Cookie-баннер.** Отсутствует. При наличии GTM и обращении к сторонним доменам
(`tella.tv`, `img.logo.dev`) это, вероятно, осознанное решение не показывать
баннер, а не отсутствие трекинга. Юридическую сторону не оцениваю.

**Что в механике сделано лучше всего.** Разница температуры между путями
выдержана: холодный посетитель получает поле для своего домена, тёплый —
кнопку, готовый к разговору — демо, а самый прогретый (досмотревший видео) —
CTA прямо под плеером. Четыре разных состояния читателя, четыре разных двери.

---

## 7. Визуал и движение

**Тема.** Тёмная, одна, без переключателя. Палитра из HTML:

- Фон: `#000000`, `#0B0B0B`, `#161616` (градиент карточек:
  `linear-gradient(97.16deg,#161616 6.48%,#000000 94.42%)`)
- Акцент: `#FF4D00` → `#E54500` / `#E64500` / `#FF6A33` (оранжевый градиент)
- Текст: `#FFFFFF`, `#DEDEDE`, `#dddddd`, `#f3f3f3`; приглушённый `#666666`
- Служебные: `#323232` (границы), `#ff4444` (бейдж `New`)

Ровно один акцентный цвет на всю страницу, и он зарезервирован за действием:
кнопки, надзаголовки секций, свечение вокруг поля ввода, искры фона. Ничто
декоративное не окрашено в оранжевый — дисциплина, которую стоит скопировать.

**Типографика.** Inter, единственная гарнитура (`font-inter` × 195). Веса:
`normal`, `medium`, `semibold`, `bold`, `extrabold`. Шкала H1 респонсивная и
задана явно: `text-[28px] sm:text-[40px] md:text-[56px] lg:text-[72px]`,
`leading-[1.2]`, `tracking-[-0.02em] md:tracking-[-3.6px]`. Отрицательный
трекинг на крупном кегле — характерная примета современного SaaS-лендинга.

**Тип визуала.** Смешанный, и распределение осмысленное:

- Фон героя — SVG-паттерн точечной сетки с оранжевыми искрами
  (`/hero-background.svg`)
- Продукт — один большой WebP (`/dashboard-preview.webp`, 5192×3132) и второй
  (`/product-features.webp`)
- Возможности — **нарисованные SVG-макеты**, а не скриншоты
  (`/features-prompts.svg`, `/features-track.svg`, `/features-analyze.svg`,
  `/features-outrank.svg`). Это позволяет держать иллюстрацию читаемой на любом
  размере и не переснимать её при каждом релизе UI.
- Иконки — локальные SVG, у декоративных `alt=""` (корректно)
- Логотипы платформ — внешний CDN logo.dev
- Люди — WebP-портреты в отзывах

**Демо продукта.** Двухминутное видео Tella в модалке, вызывается фиксированным
виджетом. Автоплей разрешён (`allow="autoplay; fullscreen"`), но только внутри
модалки — на странице ничего не играет само.

**Анимации и скролл.** Измерено по HTML:

- `transition-*` — 144 вхождения, `duration-*` — 43. То есть анимация здесь
  почти целиком **CSS-переходы на состояния** (hover, открытие аккордеона,
  появление модалки), а не скролл-скраб.
- `animate-*` (Tailwind-кейфреймы) — **0 вхождений**.
- Смена платформы в H1 — управляемая JS смена текста с инлайновым
  `style="opacity:1;filter:blur(0px)"`, то есть переход через прозрачность и
  размытие. Единственная непрерывная анимация на странице.
- Аккордеон FAQ: поворот половинки «плюса» —
  `style="transform:rotate(90deg)"` + `transition-transform duration-200`.

**Ритм.** Строгий и повторяющийся: `надзаголовок с иконкой → H2 → подзаголовок →
кнопка Start Free Trial справа → сетка контента`. Так построены Features,
Benefits, How It Works, Testimonials, Pricing, FAQ — шесть секций подряд по
одному шаблону. Разделители — пунктирные линии и вертикальные направляющие по
краям контентной колонки (видны на скриншотах), которые собирают всю страницу в
одну сетку.

**Деградация.**

- **Без JS:** вся копия на месте (SSR), кроме пяти ответов FAQ и вращения H1 —
  но `sr-only` вариант H1 отдаёт все девять платформ статически. То есть
  деградация текста продумана.
- **`prefers-reduced-motion` — 0 вхождений, `motion-reduce:` — 0 вхождений.**
  Вращение H1 и все 144 перехода не имеют спокойного режима. Для страницы, где
  главный заголовок непрерывно меняется, это заметный пробел в доступности.
- **Наблюдённый сбой:** главный скриншот продукта не отрисовался (см. раздел 4
  карты и раздел 9).

---

## 8. SEO/AEO техника

### Мета-слой

| Элемент | Значение | Оценка |
|---|---|---|
| `<title>` | `"ZeroRank | Track & Improve Your AI Search Visibility"` (52 знака) | Хорошо. Бренд + категория, укладывается в выдачу |
| `<meta description>` | `"Track and improve your visibility across AI platforms. Reach customers before your competitors do."` (98 знаков) | Хорошо. Дословно повторяет подзаголовок героя |
| H1 | `"Rank #1 in ChatGPT, Perplexity, Gemini, Google AI Mode, Google AI Overviews, Grok, Bing Copilot, Claude, DeepSeek"` (113 знаков, `sr-only`) | Один H1 на странице. Умный приём — см. раздел 10 |
| `<link rel="canonical">` | `https://zerorank.ai` | Есть |
| `<meta name="robots">` | Отсутствует → по умолчанию `index, follow` | Корректно |
| `<html lang>` | `en` | Есть |
| `hreflang` | **0 вхождений** | Сайт одноязычный — приемлемо |
| `og:title` / `og:description` / `og:url` | Есть | — |
| **`og:image`** | **ОТСУТСТВУЕТ** | **Дефект.** `twitter:image` задан (`https://zerorank.ai/dashboard-preview.webp`), а `og:image` — нет. LinkedIn, Slack, Facebook, Telegram читают `og:image`; расшаренная ссылка отдаст карточку без картинки |
| `og:type`, `og:site_name` | **ОТСУТСТВУЮТ** | Дефект помельче |
| `twitter:card` | `summary_large_image` | Есть |
| `twitter:site` | `@zerorank_ai` | Есть |
| `twitter:image:alt` | `"ZeroRank AI Search Visibility Dashboard"` | Есть — редкая аккуратность |

### Иерархия заголовков

`H1` (1) → `H2` (7) → `H3` (11) → `H5` (3, в футере).

**`H4` пропущен**: футер использует `H5` для `Sections` / `Socials` / `Pages`,
хотя ближайший предок — `H2`/`H3`. Нарушение — косметическое, но для продукта
про машинную читаемость показательное.

### Структурированные данные

**Что есть на главной** (2 блока `application/ld+json`):

```json
{"@context":"https://schema.org","@type":"Organization","name":"ZeroRank",
 "url":"https://zerorank.ai","logo":"https://zerorank.ai/logo.svg",
 "sameAs":["https://x.com/zerorank_ai","https://www.linkedin.com/company/zerorank-ai"]}
```
```json
{"@context":"https://schema.org","@type":"WebSite","name":"ZeroRank",
 "url":"https://zerorank.ai",
 "potentialAction":{"@type":"SearchAction",
   "target":"https://zerorank.ai/blog/search?q={search_term_string}",
   "query-input":"required name=search_term_string"}}
```

**Три дефекта, каждый измерен:**

1. **`logo.svg` в схеме Organization отдаёт 404.**
   `curl -o /dev/null -w "%{http_code}" https://zerorank.ai/logo.svg` → `404`,
   тело ответа — HTML со `<title>Page Not Found | ZeroRank | ZeroRank</title>`.
   То есть машиночитаемая карточка организации ссылается на несуществующий файл.
2. **Нет `FAQPage`** — при шести видимых вопросах на странице.
3. **Нет `SoftwareApplication` / `Product` / `Offer`** — при полном прайсе с
   тремя тарифами прямо на странице. Ни цена, ни триал, ни категория продукта
   не отданы машине в структурированном виде.

**И это тем заметнее, что на других своих страницах компания делает всё правильно:**

| Страница | Типы в JSON-LD |
|---|---|
| `/` (главная) | `Organization`, `WebSite`, `SearchAction` |
| `/pricing` | `Organization`, `WebSite`, `SearchAction`, **`FAQPage` с 8 парами `Question`/`Answer`** |
| `/free-tools/llms-txt-generator` | `Organization`, `WebSite`, `SearchAction`, **`WebApplication`**, **`Offer`**, **`BreadcrumbList`** (3 `ListItem`), **`FAQPage`** (2 пары) |
| `/vs/peec-ai` | `Organization`, `WebSite`, `SearchAction` — **`FAQPage` нет, хотя на странице есть `H2: "Frequently asked questions"`** |

Вывод: инфраструктура для `FAQPage` в проекте есть и работает, на главную и на
страницы сравнения её просто не поставили.

### Читается ли без JS

**Да, и хорошо — с одним крупным исключением.** 1042 слова видимого текста
извлечены из сырого HTML без исполнения JS. В HTML присутствуют: H1 целиком
(через `sr-only`), все H2/H3, вся копия Features/Benefits/How It Works, все три
отзыва с атрибуцией, полный прайс со всеми числами, финальный CTA, весь футер.

**Исключение — FAQ.** Из шести вопросов ответ в HTML есть только у одного.
Разметка закрытого пункта:

```html
<button … aria-expanded="false"><span>Do I need technical skills to use ZeroRank AI?</span>…</button>
```

— и сразу закрывающий контейнер; текста ответа между тегами нет вовсе.
Подтверждено дважды: (1) grep по сырому HTML, (2) независимо — WebFetch, который
вернул `[Answer not visible in provided content]` по пяти вопросам из шести.

То есть **пять ответов на самые частые вопросы покупателя не существуют для
краулера, для скринридера и для любой LLM, читающей страницу.** Это не
«схлопнуто и раскроется» — это отсутствие в DOM.

### Внутренние ссылки

С главной — 46 ссылок. Из футера открываются два крупных SEO-актива, которых нет
в верхней навигации: `Free Tools` и `Comparisons`.

**Sitemap: ~190 URL.** Разбор по кластерам:

| Кластер | Примерно | Примеры |
|---|---|---|
| `/free-tools/*` | ~130 | `llms-txt-generator`, `ai-crawler-url-inspector`, `chatgpt-query-fan-out-generator`, `page-token-inspector`, `robots-txt-generator-for-ai`, `schema-tester`, `ai-brand-visibility-report` |
| `/blog/*` | ~40 + 6 категорий | `aeo-vs-seo`, `geo-vs-aeo`, `geo-strategy`, `ai-citations`, `what-is-zero-click`, `chatgpt-seo`, `ai-visibility-score` |
| `/blog/*-alternatives` | 8 | `otterly-ai-alternatives`, `peec-ai-alternatives`, `scrunch-ai-alternatives`, `ahrefs-brand-radar-alternatives`, `airops-alternatives`, `promptwatch-alternatives`, `best-profound-ai-alternatives` |
| `/vs/*` | 6 | `ahrefs-brand-radar`, `promptwatch`, `scrunch-ai`, `airops`, `peec-ai`, `profound-ai` |
| Служебные | 12 | `/about`, `/pricing`, `/contact`, `/privacy`, `/terms`, `/refund`, `/book-demo`, `/newsletter`, `/zerorank-index`, `/chris-panteli` |

`robots.txt` корректен и лаконичен:

```
User-Agent: *
Allow: /
Allow: /api/media/*
Disallow: /admin
Disallow: /admin/*
Disallow: /api/*

Sitemap: https://zerorank.ai/sitemap.xml
```

`sitemap.xml` — с `lastmod` (`2026-08-27T00:21:20.306Z`), `changefreq` и
`priority` (главная `1`, блог `0.9`/`daily`).

Заголовок H1 страницы сравнения — образцовый:
`"Peec Tracks Your Visibility. ZeroRank Helps You Grow It."`

### `/llms.txt`

**404.** Ответ — HTML-страница ошибки Next.js с `<meta name="robots"
content="noindex">` и `<title>Page Not Found | ZeroRank | ZeroRank</title>`.
`/llms-full.txt` — тоже 404.

При этом в собственном каталоге бесплатных инструментов у компании есть
**`/free-tools/llms-txt-generator`** (`HTTP 200`, 106 303 байта), озаглавленный
`"Free Website LLMs.txt Generator"`, с описанием: `"Generate a properly
formatted LLMs.txt file for your website. This file helps AI models like
ChatGPT, Claude, and Perplexity better understand your business, products, and
services…"`

Компания отдаёт бесплатный генератор `llms.txt` и не имеет своего.

---

### ВЕРДИКТ: практикует ли сайт то, что продаёт?

**Частично — и разрыв проходит ровно по границе между контентом и техникой.**

**Практикует, и на высоком уровне (контентная сторона):**

1. **~190 проиндексированных URL** — почти вся площадь сайта построена под
   ответы машины: 130 бесплатных инструментов, 40 статей, 6 страниц сравнения,
   8 страниц «альтернативы конкуренту X».
2. **Покрытие цитируемых запросов сделано системно.** На каждый значимый
   конкурент — по две страницы: `/vs/peec-ai` и `/blog/peec-ai-alternatives`.
   Это ровно та форма запроса, которую LLM цитирует, отвечая «а какие есть
   альтернативы Peec AI».
3. **SSR по всему сайту** — вся продающая копия доступна без исполнения JS.
   1042 слова текста главной извлечены из сырого HTML.
4. **`sr-only`-вариант H1**, отдающий машине все девять платформ, пока человек
   видит вращающуюся анимацию. Это осознанная работа на извлекаемость.
5. **`robots.txt` и `sitemap.xml`** — корректны, с `lastmod`.
6. **Полноценная схема на страницах инструментов**: `WebApplication` + `Offer` +
   `BreadcrumbList` + `FAQPage`.

**Не практикует (техническая сторона, на самой главной):**

1. **`/llms.txt` → 404**, при том что компания раздаёт бесплатный генератор
   `llms.txt` со словами `"This file helps AI models like ChatGPT, Claude, and
   Perplexity better understand your business"`. Самое наглядное расхождение
   слова и дела на всём сайте.
2. **Пять из шести ответов FAQ отсутствуют в HTML.** Продукт продаёт извлекаемые
   ответы; собственные ответы главной страницы не извлекаются. Причём инструмент
   `/free-tools/faq-generator` у компании тоже есть.
3. **Нет `FAQPage` на главной**, хотя на `/pricing` она есть с 8 парами Q&A —
   то есть это не «не умеем», а «не поставили».
4. **Нет `Product` / `SoftwareApplication` / `Offer`** при полном прайсе на
   странице. Цена, триал и категория продукта машине не отданы.
5. **`logo.svg` в схеме Organization отдаёт 404** — карточка организации
   ссылается на несуществующий файл. Компания при этом раздаёт
   `/free-tools/schema-tester`.
6. **Нет `og:image`, `og:type`, `og:site_name`** — расшаренная в Slack или
   LinkedIn ссылка приходит без картинки.
7. **Пропущен уровень `H4`** в иерархии заголовков.

**Формулировка вердикта для плейбука.** ZeroRank выигрывает AEO **стратегией**
(площадь, форма запросов, SSR) и проигрывает его **на собственной витрине**:
шесть перечисленных дефектов — это в сумме несколько часов работы, и каждый из
них компания умеет чинить, потому что уже починила его на другой своей странице
или продаёт инструмент для его починки. Урок переносимый и неприятный: *команда,
продающая техническую дисциплину, применяет её к контенту клиента раньше, чем к
собственному `<head>`.*

---

## 9. Слабые места

**1. Пять из шести ответов FAQ не существуют для машины.**
`<button … aria-expanded="false"><span>Is my data secure?</span>` — и никакого
текста ответа в DOM. Не найдут ни краулер, ни скринридер, ни LLM. Для продукта
про AEO это дефект по существу, а не по форме.

**2. `/llms.txt` → 404 при наличии `/free-tools/llms-txt-generator`.**
Единственный факт разбора, который конкурент может процитировать дословно.

**3. Главный скриншот продукта не отрисовался.**
`/dashboard-preview.webp` (`HTTP 200`, 314 700 байт, 5192×3132) предзагружается
с `fetchPriority="high"`, но на его месте в браузере — пустой чёрный
прямоугольник высотой примерно в экран. Воспроизведено дважды. Между обещанием
героя и логотипной плашкой стоит пустота там, где должно быть главное
доказательство существования продукта.

**4. `logo.svg`, на который ссылается схема Organization, отдаёт 404.**

**5. Шесть разных надписей для двух действий.**
`Start Free Trial` (7) / `Start for Free` (2) / `Start for free` (1) — три
записи одного действия, различающиеся в том числе регистром. Плюс
`Request Demo` / `Book a Demo` — две записи другого. Одно действие должно
называться одним именем во всех местах.

**6. `1k+ marketers` против `1000+ brands`.**
Герой: `"Trusted by 1k+ marketers"`. Модалка: `"Join 1000+ brands already
tracking their AI visibility."` Одно число, две записи, две разные единицы
(люди и компании). Читатель, заметивший это, перестаёт верить обоим.

**7. `7-day free trial` спрятан в модалке.**
Единственное место на странице, где назван срок триала, — блок под видео,
который увидит только тот, кто открыл демо. Семь кнопок `Start Free Trial` на
странице не говорят, насколько free и насколько trial.

**8. Числа результата не имеют методики.**
`3x`, `225%+`, `4.6x` — что именно измерялось, от какой базы, за какой период
(срок указан только у одного из трёх: `"Within two months"`). Продукт продаёт
измерение; собственные числа не определены.

**9. `Secure and compliant` и `99.9% uptime` — чистая декорация.**
Ни стандарта (SOC 2 / GDPR / ISO), ни ссылки на status-страницу, ни SLA.

**10. Тарифы визуально неразличимы.**
Три списка одинаковой длины с одинаковыми строками; отличия зашиты в числа
внутри пунктов (`4,500` / `13,500` / `31,500+`). Сравнительной таблицы нет.
Читатель должен сличать три колонки глазами.

**11. Пустые формулировки ровно там, где обещан главный результат.**
`"Leverage insights to publish, optimize and outrank your competitors"` — это
шаг 3 из трёх, тот самый, ради которого покупают. Шаги 1 и 2 конкретны, шаг 3
абстрактен. Туда же: `"Turn Insights Into Action"`, `"Strengthen Your Brand
Authority"` / `"Build the signals AI relies on"` — какие сигналы, не сказано
нигде на странице.

**12. Нет `prefers-reduced-motion`.**
0 вхождений при непрерывно вращающемся H1 и 144 CSS-переходах.

**13. Мелкие копирайтерские огрехи, видные глазу.**
`"FAQ's"` — апостроф во множественном числе. `"…and your ranking - all in one
dashboard."` — дефис вместо длинного тире при 13 длинных тире в соседних
строках. Смешанные апострофы (1 типографский против 6 прямых).

**14. Нет `og:image`.**
Ссылка, расшаренная в Slack, LinkedIn или Telegram, придёт без превью.

**15. Ни одного проверяемого внешнего бейджа.**
G2 и AppSumo, где у продукта есть публичный рейтинг, на странице не упомянуты, —
при том, что чужой рейтинг проверяем, а `1k+` нет.

---

## 10. Переносимые приёмы

Каждое правило — формулировка + дословный пример отсюда.

**Общие приёмы**

**1. Обещай позицию, а не инструмент.**
Заголовок называет место, которое покупатель хочет занять, а не то, что вы ему
дадите.
> `"Rank #1 in ChatGPT"` — не «отслеживайте видимость в ИИ-поиске».

**2. Перечисляй площадки поимённо — список делает абстракцию осязаемой.**
Девять названий в H1 работают лучше любого объяснения, что такое ИИ-поиск.
> `"Rank #1 in ChatGPT, Perplexity, Gemini, Google AI Mode, Google AI Overviews, Grok, Bing Copilot, Claude, DeepSeek"`

**3. Отдавай машине полный список, человеку — короткую анимацию.**
Приём, который стоит унести целиком: `sr-only`-span с полным перечислением +
`aria-hidden` на визуальной части + `aria-live="polite"` на вращающейся.
> ```html
> <h1><span class="sr-only">Rank #1 in ChatGPT, Perplexity, …, DeepSeek</span>
> <span aria-hidden="true">Rank #1 in</span>
> <span aria-live="polite" aria-atomic="true">ChatGPT</span></h1>
> ```
> Человек видит 18 знаков, краулер получает 113. Оба довольны.

**4. Замени кнопку на поле ввода — превращай «зарегистрируйся» в «посмотри на себя».**
Первый шаг требует любопытства, а не обязательства.
> `<input placeholder="your-website.com" name="url">` + кнопка `Analyze`,
> вместо `Sign up` в герое.

**5. Под каждым CTA — снятие ОДНОГО возражения, и у разных CTA возражения разные.**
Не повторяй один и тот же аргумент; расходуй их по одному.
> Герой: `"Setup in 2 mins"` · `"No credit card required"` (время, деньги).
> Модалка: `"7-day free trial"` · `"Cancel anytime"` (срок, обязательство).
> Футер: `"Secure and compliant"` · `"99.9% uptime"` (безопасность, надёжность).

**6. Опиши одну механику дважды: языком функций и языком исходов.**
Одна и та же четвёрка, два пересказа — для скептика и для покупателя.
> Features: `"Track Your AI Rankings"` → Benefits: `"Win More AI Recommendations"`.
> Features: `"Outrank Your Competitors"` → Benefits: `"Move Before Competitors Do"`.

**7. Ставь метрику ПЕРЕД цитатой, а не после.**
Крупное число ловит взгляд, цитата его объясняет, подпись подтверждает.
> `3x` / `mention growth` → `"ZeroRank changed how we approach AI search."` →
> `"…Within two months, our mentions grew 3x."` → **Ervis Bregasi, CEO, ClickFlare**

**8. Пусть логотипы и отзывы подкрепляют друг друга.**
Три из пяти логотипов плашки — те же компании, что дали именные отзывы ниже.
Логотип без цитаты декоративен; логотип с цитатой — доказательство.
> Плашка: `ClickFlare`, `AdPlexity`, `LanderLab` → они же в отзывах ниже.

**9. Приклей CTA к концу демо-видео.**
Самый прогретый человек на сайте — тот, кто только что досмотрел двухминутное
демо. Не отпускай его обратно на страницу.
> Внутри видео-модалки, прямо под плеером Tella:
> `"Ready to dominate AI search?"` / `"Join 1000+ brands already tracking their
> AI visibility."` / `"7-day free trial" · "Cancel anytime"` / `Start for free`

**10. Держи один акцентный цвет и трать его только на действие.**
Оранжевый `#FF4D00` на чёрном: кнопки, надзаголовки секций, свечение поля
ввода. Ничего декоративного в акцентном цвете нет.

**11. Держи все заголовки короче 45 знаков.**
Медиана H2 здесь — 37 знаков / 6 слов, максимум — 45. Норма выдержана без
единого исключения.
> `"Get Started in Minutes"` (22) · `"Turn AI Visibility Into Customer Growth"` (39)

**12. Один повторяющийся шаблон секции, шесть раз подряд.**
`надзаголовок с иконкой → H2 → подзаголовок → CTA справа → сетка`. Скучно на
макете, отлично при чтении: читатель учится структуре один раз.

**13. Пиши во втором лице; продукт как подлежащее — не больше двух раз на страницу.**
> `"Track where your brand appears, why it doesn't, and what to improve next."`
> — а не «наша платформа отслеживает…».

**14. Срочность строй на конкуренте, а не на таймере.**
Ни одного дедлайна на странице; вместо него одна и та же мысль, проведённая
пять раз.
> `"Reach customers before your competitors do."` · `"spot new opportunities
> before your competitors"` · `"Move Before Competitors Do"` · `"get notified
> when you're slipping behind"` · `"ZeroRank AI helps you act before your
> competitors do."`

**15. Пусть о боли говорит клиент, а не копирайтер.**
Самая сильная формулировка проблемы на странице — в чужих кавычках.
> `"We went from manually checking prompts for hours to having everything in
> one place."`

**16. Назови единицу тарификации прямым текстом.**
В категории, где все продают «кредиты», конкретика сама по себе — аргумент.
> `"Up to 4,500 AI answers analyzed per month"` · `"15 Prompt Research runs per month"`

**17. Строй лестницу обещаний: чем ближе к кнопке, тем ближе к деньгам.**
> H1: `"Rank #1 in ChatGPT"` (позиция) → подзаголовок: `"Track and improve your
> visibility"` (видимость) → финальный CTA: `"Ready to win more customers
> through AI search?"` (клиенты).

**18. Вынеси соцдоказательство в главное меню.**
Два пункта первого уровня заняты доверием: `Clients` и `Wall of Love`.

**19. Дай разные двери разной температуре читателя.**
Четыре состояния — четыре пути: холодный получает поле для домена, тёплый —
кнопку, готовый к разговору — `Request Demo`, досмотревший видео — CTA под
плеером.

**20. Рисуй интерфейс в SVG, а не снимай его.**
Карточки Features содержат нарисованные макеты (`/features-track.svg` с
диаграммой `58% / 41% / 29%`), а не скриншоты: читаемо на любом кегле и не
устаревает с каждым релизом UI.

---

### Отдельно: приёмы продажи НОВОЙ категории, которую покупатель ещё не ищет

**N1. Заимствуй ментальную модель из старой категории — не объясняй новую.**
`"Rank #1 in"` — готовая, полностью освоенная концепция из SEO, перенесённая на
новую территорию. Продавать новое как «старая задача в новом месте» дешевле, чем
объяснять с нуля. Ни слова «paradigm», «new era», «the future of».

**N2. Легитимизируй категорию метрикой, а не манифестом.**
Свыше 30 числовых утверждений на 1042 слова — одно число на 35 слов. У явления
есть единица измерения (`AI answers analyzed`), тариф ($76) и дашборд — значит,
оно существует. Это и есть весь аргумент; отдельного объяснения «почему AEO
важен» на странице нет вовсе.

**N3. Назови площадки поимённо — это дешёвый способ доказать существование категории.**
Девять названий в H1 и `17 AI platforms` пять раз по тексту. Читатель, который
не знал, что у него есть проблема, узнаёт о ней из списка мест, где его может
не быть.

**N4. Держи аббревиатуры категории ВНЕ главной, а поисковый спрос по ним лови блогом.**
`AEO` и `GEO` на главной — 0 вхождений (проверено). При этом
`/blog/aeo-vs-seo`, `/blog/geo-vs-aeo`, `/blog/geo-strategy` существуют.
Главная говорит описательно — для тех, кто ещё не знает термина; блог ловит тех,
кто уже ищет по нему.

**N5. Не пугай гибелью — пугай отставанием.**
Ни одного апокалиптического утверждения. Страх ровно один и всегда относительный:
> `"Reach customers before your competitors do."`
Читателю не нужно принимать мрачную картину мира — достаточно допустить, что
кто-то шустрее. Порог согласия несравнимо ниже.

**N6. Дай бесплатно посмотреть на СЕБЯ до всякой регистрации.**
В категории без сформированного спроса «мне это нужно?» — главное возражение, и
снимается оно только персональными данными о самом читателе.
> `placeholder="your-website.com"` + `Analyze`, без карты и без аккаунта.

**N7. Сделай ИИ действующим лицом с предпочтениями.**
Риторический фундамент всей категории: не инструмент, а привратник, которого
нужно расположить к себе.
> `"Be the brand AI chooses when buyers compare options."` · `"See how AI is
> talking about your brand"` · `"Build the signals AI relies on when
> recommending brands."`

**N8. Захватывай «альтернативы конкуренту X» ДВУМЯ страницами на каждого.**
Для новой категории именно этот тип запроса LLM цитирует чаще всего.
> `/vs/peec-ai` (`H1: "Peec Tracks Your Visibility. ZeroRank Helps You Grow It."`)
> **и** `/blog/peec-ai-alternatives` — по паре на каждого из шести конкурентов.

**N9. Раздавай бесплатные инструменты категории — они и трафик, и доказательство экспертизы.**
~130 страниц `/free-tools/*`, из них половина — прицельно про AEO
(`llms-txt-generator`, `ai-crawler-url-inspector`,
`chatgpt-query-fan-out-generator`, `page-token-inspector`,
`robots-txt-generator-for-ai`). Инструмент, который решает кусочек новой задачи
бесплатно, доказывает, что задача реальна.

**N10. Вбрасывай термины категории в плашку анонса — для опытного сегмента.**
Плашка над H1 говорит на языке тех, кто уже внутри темы, не мешая новичку
читать H1.
> `"Introducing Gap Opportunities and Fanout Query Analytics. Try it now →"`

**N11. И главное правило, выведенное из их же ошибки: продавая дисциплину, применяй её к себе первым.**
Компания раздаёт `/free-tools/llms-txt-generator` и не имеет собственного
`/llms.txt` (404). Продаёт извлекаемые ответы — и держит пять из шести ответов
FAQ вне DOM. Раздаёт `/free-tools/schema-tester` — и ссылается в схеме
Organization на `logo.svg`, который отдаёт 404. В категории, продающей
техническую дисциплину, собственная витрина — это демо-версия продукта, и
проверять её нужно строже клиентской.

---

## 11. Что не удалось проверить

1. **Что происходит после отправки формы `Analyze`.** Форму не отправлял.
   Гипотеза (перенос домена в регистрацию на `app.zerorank.ai`) со страницы не
   подтверждается — **не проверено.**
2. **Содержимое пяти закрытых ответов FAQ.** Их нет в DOM; аккордеон не
   раскрывал, чтобы не запускать клиентские обработчики. Возможно, ответы
   подгружаются по клику из JS-бандла — **не проверено**, из какого источника.
3. **Содержимое двухминутного демо-видео Tella.** Не смотрел.
4. **Реальность отзывов.** Имена, должности и компании не сверял с LinkedIn —
   **не проверено.**
5. **Методика чисел `3x`, `225%+`, `4.6x`.** На странице не раскрыта; за
   пределами страницы не искал.
6. **Действительно ли `1k+ marketers` и `1000+ brands` — одно число.**
   Внутренних данных нет; зафиксирована только нестыковка формулировок.
7. **Страницы `/clients`, `/wall-of-love`, `/about`, `/blog`, `/book-demo`,
   `/free-tools` (каталог), `/zerorank-index`.** Не открывал; о них известно
   только из sitemap и футера.
8. **Причина, по которой `/dashboard-preview.webp` не отрисовался.** Установлено,
   что файл существует (`HTTP 200`, 314 700 байт, 5192×3132) и что область пуста
   в двух независимых загрузках. Является ли это несработавшим scroll-reveal,
   провалом декодирования картинки шириной 5192 px, ошибкой JS или особенностью
   конкретного профиля Chrome — **не проверено** (консоль и сеть не снимал).
9. **Мобильная версия.** Все замеры — десктоп 1568×780. Респонсивные классы в
   HTML присутствуют (`sm:`, `md:`, `lg:`), но на устройстве не проверялась.
10. **Core Web Vitals, LCP, реальная скорость отрисовки.** Замерен только
    `time_total = 0,553 с` для HTML-документа; Lighthouse не запускал.
11. **A/B-тесты.** В HTML не обнаружены следы Optimizely/VWO/GrowthBook и т. п.,
    но серверный сплит на Vercel Edge был бы невидим — **не проверено.**
12. **Наличие чата в продукте.** `"Email + Live Chat Support"` заявлен в тарифах;
    виджета на лендинге нет. Есть ли чат внутри приложения — **не проверено.**
13. **Юридическая корректность отсутствия cookie-баннера** при активном GTM.
    Не оценивал.
14. **Внешние данные о позиционировании** (G2: «альтернативы — SOCi, Semrush,
    Writesonic»; AppSumo: рейтинг 4.9 при 39 отзывах) взяты из веб-поиска, а не
    со страницы, и **самостоятельно не верифицированы.**
15. **Побочное наблюдение, не относящееся к ZeroRank.** В ходе браузерного
    прохода вкладка однократно оказалась на стороннем домене `crowdreply.io`
    (конкурент в той же категории) без навигации с моей стороны. Причину
    установить не удалось — **не проверено**; на выводы разбора не влияет,
    контент того сайта в отчёт не включён.
