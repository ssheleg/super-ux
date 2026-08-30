# Разбор лендинга: CrowdReply

> Форензический разбор для playbook «как строить лендинги». Каждое утверждение
> подкреплено verbatim-цитатой, HTML-фрагментом или измерением. Где доказательства
> нет — стоит явная пометка **не проверено**.
> Цитаты приведены в оригинале (английский), анализ — по-русски.

---

## 0. Паспорт

| Поле | Значение | Чем подтверждено |
|---|---|---|
| URL | `https://crowdreply.io/` | — |
| Дата снятия | 2026-08-30 | — |
| Дата публикации страницы | `<!-- Published Aug 21, 2026, 5:12 PM UTC -->` | комментарий в HTML, строка 3 |
| Как снято | `curl` (сырой HTML), WebFetch (рендер-текст), Chrome (3 скриншота, вкладка закрыта), плюс `curl` по `/pricing`, `/casestudy`, `/demo`, `robots.txt`, `sitemap.xml`, один WebSearch для рыночного контекста | — |
| SSR или CSR | **SSR** — статический экспорт Framer. Весь продающий текст присутствует в сыром HTML без JS | `curl` + grep: заголовки, подзаголовки, отзывы, FAQ-вопросы читаются из HTML |
| Вес HTML | **1 140 808 байт (1,09 МБ)** одного документа | `curl -w "%{size_download}"` → `1140808`; `wc -c` → `1140808` |
| Время ответа | 0,77 с (TTFB+загрузка, один запрос) | `curl -w "%{time_total}"` → `0.772035s` |
| Конструктор | **Framer**, `<meta name="generator" content="Framer 77cb752">`; главный бандл `framerusercontent.com/sites/5QSqmBc7w5PfOa3CbxSCWJ/script_main.CU8-U03q.mjs` | HTML `<head>` |
| Шрифты | `Inter Tight` и `DM Mono` в `@font-face`; заголовки — **Outfit** (`--font-selector:RlM7T3V0Zml0LXJlZ3VsYXI=` → base64 «FS;Outfit-regular») | инлайн-CSS |
| Продукт в одном предложении | Платформа отслеживания видимости бренда в ИИ-поиске (ChatGPT, Perplexity, Gemini, Claude), **со встроенным «Engagement Engine»** — сервисом, который сам пишет и публикует комментарии от вашего имени на Reddit/Quora/Facebook, плюс маркетплейс покупных редакционных ссылок | `<meta name="description">`, секция «Meet the Engagement Engine», `/pricing` |
| ICP | B2B/SaaS-маркетологи и агентства; на `/pricing` — «For teams getting started…», «For scaling teams…», «For organizations running AI visibility and engagement at scale» | `/pricing` |
| Цена | **На лендинге отсутствует.** На `/pricing`: Starter **$99/mo**, Growth **$299/mo**, Enterprise **from $499/mo** | `curl_pricing`: `h2 \| $99`, `h2 \| $299`, `h2 \| $499` |

### Стек и growth-обвязка (полный список найденного)

| Инструмент | Идентификатор / доказательство | Что означает |
|---|---|---|
| Google Tag Manager | `GTM-NLP74GHQ` (+ `<noscript>` iframe в `bodyStart`) | контейнер-зонтик; конкретные пиксели внутри него **не проверены** |
| PostHog | `posthog.init('phc_osZj3PACSnhnkMpRMf3SYCc2JeLtKq24gLMdyCSZ9r6P', { api_host: '/ingest', ui_host: 'https://us.posthog.com', defaults: '2026-01-30', person_profiles: 'identified_only', capture_pageview: 'history_change', custom_campaign_params: ['utm_id'], capture_exceptions: false, disable_surveys: true })` | продуктовая аналитика через **обратный прокси `/ingest`** (обход блокировщиков). Feature flags доступны в SDK → A/B-тесты технически возможны, но **факт их использования не проверен**. Опросы выключены, отлов исключений выключен |
| Meta Pixel | `fbq('init', '757690197138400'); fbq('track', 'PageView');` | ретаргетинг Facebook/Instagram |
| FirstPromoter | `fpr("init", {cid:"sh423r4p"}); fpr("click");` + `cdn.firstpromoter.com/fpr.js` | партнёрская программа (в футере есть `/affiliates`) |
| Собственный трекер | `https://tracking.crowdreply.io/v1/lst/universal-script?ph=4e6a…&tag=!clicked&ref_url=` | first-party атрибуция кликов на своём домене |
| Crisp | `window.CRISP_WEBSITE_ID="651172e1-7823-490d-b086-b91dc4e3159a"` | чат-виджет, sticky в правом нижнем углу (виден на скриншотах) |
| Framer Analytics | `https://events.framer.com/script?v=2` | базовая аналитика конструктора |
| Cookie-баннер | **отсутствует** | grep по `cookieyes\|cookiebot\|osano\|termly\|consent` → 0 совпадений |
| Session recording | **не проверено** — SDK PostHog умеет, но `startSessionRecording` в init не вызывается; включение может быть на стороне проекта |
| Отдельный A/B-инструмент | **отсутствует** — нет VWO, Optimizely, Google Optimize | grep → 0 |

---

## 1. Карта секций (по порядку)

Framer рендерит **три брейкпоинт-варианта** одного и того же блока в SSR-HTML
(desktop/tablet/mobile), поэтому сырые счётчики элементов утроены. Ниже —
дедуплицированная карта. Всего уникального копирайта на странице: **175 строк,
1090 слов** (измерено скриптом по дедуплицированному тексту).

### 1.0 Announcement bar (верхняя полоса)
- **Заголовок:** `Backlinks Marketplace is live: Buy vetted backlinks from 40k+ publishers that actually move rankings →`
- **Подзаголовок:** нет
- **CTA:** `Browse Catalogue` → `https://crowdreply.io/features/backlinks-marketplace`
- **Визуал:** тонкая тёмная полоса над шапкой, стрелка `→` в конце текста
- **Работа в аргументе:** анонс нового модуля; вытягивает трафик на самую монетизируемую фичу ещё до первого экрана. Заодно сигнализирует «продукт живой, релизы идут».

### 1.1 Навигация
- **Пункты (verbatim):** `Features` (dropdown) · `Pricing` · `Case Studies` · `Resources` (dropdown) · `Outreach` + бейдж `NEW` · `Login`
- **CTA:** `Login` — тёмная кнопка справа
- **Визуал:** плавающая «таблетка» (pill) со скруглением, отделённая от края экрана; логотип CrowdReply слева
- **Работа в аргументе:** **в шапке нет коммерческого CTA** — только `Login`. Вся конверсия отдана телу страницы. Бейдж `NEW` на `Outreach` — дешёвый сигнал скорости разработки.

### 1.2 Hero (первый экран)
- **Бейдж / H1 (verbatim):** `#1 AI Search Visibility Tool` — где `#1` залит градиентом. **Это единственный `<h1>` на странице, и он же обёрнут в `<a href="./">`.**
- **Визуальный заголовок (verbatim, два `<h2>`):** `Make` + встроенный ряд иконок ИИ-моделей + `Mention Your Brand`
  - HTML: `<h2 …>Make</h2>` → `<div data-framer-name="AI models-icons">` c четырьмя SVG, чьи родители названы `Google`, `OpenAI`, `perplexity-fill`, `claude-line` → `<h2 …>Mention Your Brand</h2>`
  - То есть читается как: **«Make [ChatGPT, Gemini, Perplexity, Claude] Mention Your Brand»** — логотипы работают как существительное в предложении.
- **Подзаголовок (verbatim):** `Track your AI search visibility. Engage where AI pulls its answers. Become the brand AI recommends.`
- **CTA:** два — `Book a demo` (чёрная кнопка) и `Start 7 day free trial` (оранжевая, primary)
- **Микро-элемент:** `See your AI Visibility Score` (`<h6>`) внутри блока с именем `data-framer-name="Input"` и иконкой `line-chart-line`
- **Визуал:** светло-кремовый фон; по краям экрана — логотипы источников (Quora, Reddit, LinkedIn, Wikipedia, Facebook, Instagram), соединённые тонкими закруглёнными линиями с центром. Это диаграмма «вот откуда ИИ берёт ответы, и мы стоим на всех этих узлах».
- **Работа в аргументе:** заявляет категорию (`AI Search Visibility Tool`), обещание (`Mention Your Brand`) и механизм (иконки моделей + логотипы площадок) **за один экран, без единого абзаца объяснений**.

### 1.3 Стек продуктовых карточек (под hero)
Три карточки, раскрывающиеся при скролле:
| Эйбрау | Заголовок (verbatim) | Подзаголовок (verbatim) |
|---|---|---|
| `AI Search` | `See How AI Ranks Your Brand` | `Track visibility and ranking shifts across popular models. See which sources AI cites — and where you're missing.` |
| `Social Listening` | `Listen Before AI Does` | `Find conversations early, get your brand mentioned before AI picks them up.` |
| `AI Backlinks Marketplace` | `AI Backlinks Marketplace` | `Buy editorial backlinks from a vetted catalog of 40,000+ publishers with real authority and traffic data on every site. Order in minutes, track every placement until the link is live.` |
- **Визуал:** реальные тёмные скриншоты продукта на светлых карточках. В карточке маркетплейса — таблица с настоящими доменами (`retrododo.com` — Computer & Video Games, DR 57, 116.9K трафика; `hotair.com` — Business News, DR 72, 50.4K), флагами стран и **замазанными блюром ценами** («From $XX»). Пагинация `Page 2 of 16`, `7 / page`.
- **Работа в аргументе:** три продукта = три причины купить; блюр на ценах — механика «зарегистрируйся, чтобы увидеть».

### 1.4 Видео-карточка
- **Заголовок (verbatim):** `CrowdReply in 90 Seconds ✨`
- **Подзаголовок (verbatim):** `Click on the video thumbnail to view.`
- **CTA:** `Get started` → `/signup`
- **Визуал:** оранжевая карточка, тёмный превью-кадр, кнопка `▶ Click to view`. Видео **не встроено** — грузится по клику (экономия на LCP).
- **Работа в аргументе:** демо для тех, кто не хочет читать. Ограничение «90 секунд» снимает страх потерянного времени.

### 1.5 Соцпруф-полоса
- **Элементы (verbatim):** бейдж G2 с пятью звёздами и числом `4.9` (ссылка на `https://www.g2.com/products/crowdreply/reviews`) + строка `Trusted by 5,000+ brands`
- **Ниже:** карусель логотипов + карусель кейсов, каждый с надписью `CASE STUDY`, ведущей на `./casestudy/<company>`: **respeecher, stingrai, safegraph, pabau, lido, taxdome, lemlist**
- **Логотипы (из alt-атрибутов):** `Xbert intelligence`, `wodify`, `Stripo`, `Omio`, `NP Digital`, `Levanta`, `Kamatera`, `instantly`, `figr`, `facetune`, `Creatio`, `Alvao`
- **Работа в аргументе:** единственный на странице **проверяемый** блок доверия — рейтинг ведёт на внешний источник, кейсы на отдельные страницы с названными компаниями.

### 1.6 Проблема
- **Эйбрау:** `Problem`
- **Заголовок (verbatim):** `AI is the new search engine. Are you visible?`
- **Подзаголовок (verbatim):** `ChatGPT, Perplexity, Gemini and others are replacing Google for buying decisions. They pull answers from community discussions, review sites, and editorial content. The brands in those sources get recommended. The rest get ignored.`
- **CTA:** нет
- **Визуал:** слева текст, справа стопка «карточек-промптов» с иконками моделей: `Best CRM for B2B companies?` (Google), `Top alternatives to HubSpot` (OpenAI), `Free design tools for beginners` (Claude, приглушённая). Всего шесть промптов в ротации: + `What payroll tool do startups use?`, `Top analytics tools for ecommerce`, `Easy design tools for non designers`.
- **Работа в аргументе:** **лучшая секция страницы.** Формулирует врага (Google→ИИ), механизм (ИИ тянет ответы из сообществ) и ставку в двух предложениях-приговорах: `The brands in those sources get recommended. The rest get ignored.` Промпты — реальные покупательские запросы, читатель узнаёт в них свою категорию.

### 1.7 Engagement Engine (ключевая дифференциация)
- **Эйбрау:** `Your Competitive Moat`
- **Заголовок (verbatim):** `Meet the Engagement Engine`
- **Подзаголовок (verbatim):** `Other tools show you where you're missing. CrowdReply gets you in.`
- **Шаги (verbatim):**
  1. `Find High-Impact Conversations` — `Surface threads across Reddit, Quora, Wikipedia, and blog sites — filtered by relevance and AI citation potential.`
  2. `Craft Your Response` — `Write your own or let AI generate a reply matched to context.`
  3. `We Post for You` — `Posted through trusted community profiles on your behalf.`
  4. `Never Miss a New Conversation` — `Spot emerging threads in real time. Get in before AI picks them up.`
- **CTA:** нет (внутри — декоративная кнопка `Submit comment` в макете продукта)
- **Визуал:** анимированная схема с узлом `Your Brand` в центре; список тредов с реальными объёмами трафика: `Best CRM for startups — 2.3k Visitors/mo`, `Top project management tools — 3.3k Visitors/mo`, `Slack alternatives — 2k Visitors/mo`, ещё девять.
- **Работа в аргументе:** **весь позиционный вес страницы держится здесь.** Одна фраза, `Other tools show you where you're missing. CrowdReply gets you in.`, отделяет их от всей категории AEO-трекеров. Четыре шага делают невидимый сервис (люди пишут комментарии от вашего имени) осязаемым.

### 1.8 Аналитический слой
- **Эйбрау:** `AI Search`
- **Заголовок (verbatim):** `The Intelligence Layer Behind Your AI Presence`
- **Подзаголовок (verbatim):** `Monitor every AI model, track citation sources and spot opportunities before competitors.`
- **Четыре карточки (verbatim):**
  - `AI Search Visibility Tracking` — `Track your visibility score across ChatGPT, Perplexity, Gemini, and Claude. Benchmark against competitors and monitor ranking shifts over time.`
  - `Prompt Tracking` — `Track which prompts trigger your brand in AI answers. See frequency, trends, and competitor coverage.`
  - `Powerful Reporting` — `Shareable reports for stakeholders and clients. Export visibility trends, citation data, and engagement ROI.`
  - `Citation Source Intelligence` — `See which domains AI models cite for your category. Find gaps where competitors appear and you don't.`
- **CTA:** нет
- **Визуал:** тёмные скриншоты дашборда внутри светлых карточек. На скриншоте видно `LLM Visibility Score & Ranking`, `10%`, `↑ 0.48% vs previous day`, `#8 Your rank`, график с градиентной линией.
- **Работа в аргументе:** закрывает возражение «а вы вообще измеряете или просто спамите». Упоминание `for stakeholders and clients` — прицел в агентства.

### 1.9 Маркетплейс ссылок
- **Эйбрау:** `Backlinks Marketplace`
- **Заголовок (verbatim):** `AI Backlinks Marketplace`
- **Подзаголовок (verbatim):** `Editorial backlinks from 40,000+ vetted publishers. The authority footprint that gets your brand cited in AI answers.`
- **Три подпункта (verbatim):**
  - `Build the authority AI trusts` — `AI models cite the sources that real publications link to. Backlinks and brand mentions build the footprint those citations draw from.`
  - `40,000+ vetted partner publishers` — `We partner directly with each publisher, and every listing clears authority, traffic, and spam checks before you see it.`
  - `Ordered in minutes, not months` — `Skip outreach entirely. Add placements to your cart, let AI auto fill each brief, and watch every link move to live.`
- **CTA:** `Start Ordering` → `/signup`
- **Работа в аргументе:** второй источник выручки. Формула каждого подпункта — «возражение → снятие»: доверие (`vetted`), скорость (`minutes, not months`), связь с главным обещанием (`the authority AI trusts`).

### 1.10 Social Listening
- **Эйбрау:** `Social Listening`
- **Заголовок (verbatim):** `Always Listening. Always First.`
- **Подзаголовок (verbatim):** `Track and engage on every discussion that could shape how AI sees your brand.`
- **Четыре карточки (verbatim):** `Ranked Threads` (`Threads already pulling thousands of visitors. Your brand needs to be on them.`) · `New Threads` (`Be the first to show up in conversations your competitors haven't seen yet.`) · `Single Search` (`Not ready for always-on monitoring? Search once, find what matters, move on.`) · `Alerts` (`Get notified the moment a conversation worth joining appears. Email or Slack.`)
- **CTA:** нет
- **Работа в аргументе:** `Single Search` — единственная на всей странице карточка, написанная **под сомневающегося**: «не готов к подписке — попробуй разово». Прямое снятие возражения внутри фичи.

### 1.11 Отзывы
- **Эйбрау:** `Testimonials`
- **Заголовок (verbatim):** `Don't Take Our Word for It`
- **Подзаголовок (verbatim):** `See how teams are turning AI search gaps into competitive advantages.`
- **Метрики-плитки (verbatim):** `Increased LLM visibility +47%` · `Citations coverage 75%` · `Share of voice 4%` · `2X Increased sales`
- **Отзывы (verbatim, полностью):**
  1. `"I've never seen such huge ROAS anywhere else. I was able to take my e-com stores to rank in almost all of our core topics in our niche, which has led to over $1M extra revenue since January."` — **Marcus A**, `eCom`
  2. `"The tool really made our work so much easier, we're able to give our clients not only good results, but with less effort from our side. We're been with CrowdReply since they started, primarily for Reddit marketing, but now we're also able to offer AI visibility to our clients"` — **Michal H**, `Red-engage`
  3. `"Our app launched 4 months ago and ranking on LLM's have driven more traffic than paid ads for us. We've tried to get our brand into all the relevant Reddit citations that we see LLM's citing from"` — **Adrina W**, `App`
  4. `"We've had an incredible ROI using CrowdReply at our app, Optimal Bet. In fact, it's our best marketing channel!!"` — **Patrick**, `Optimal Bet`
- **Работа в аргументе:** должна закрывать доверие — **закрывает слабее всех остальных секций** (разбор в §5 и §9).

### 1.12 FAQ
- **Эйбрау:** `FAQ`
- **Заголовок (verbatim):** `Frequently Asked Questions`
- **Подзаголовок (verbatim):** `Get answers to common questions here`
- **Восемь вопросов (verbatim):** `What is CrowdReply?` · `Why does AI search visibility matter for my brand?` · `How does CrowdReply improve my AI search rankings?` · `Which AI models do you track?` · `What platforms can I engage on?` · `How much does CrowdReply cost?` · `Can I try CrowdReply for free?` · `Can I use the platform to only engage on social platforms?`
- **Ответ в HTML присутствует только у первого:** `CrowdReply is the AI search visibility platform that helps brands monitor, engage, and grow their presence across AI search engines like ChatGPT, Perplexity, Gemini, and Claude. We track how AI models see your brand, identify the citation sources they pull from, and give you the tools to engage on those platforms — so your brand becomes the one AI recommends. We combine analytics, social listening, and our proprietary Engagement Engine into one platform.`
- **Работа в аргументе:** порядок вопросов — воронка возражений: что это → зачем → как работает → покрытие → площадки → **цена** → бесплатно ли → можно ли только часть. Цена и «бесплатно» стоят на 6-й и 7-й позиции, ровно там, где их задаёт готовый к покупке.

### 1.13 Финальный CTA
- **Заголовок (verbatim, `<h2>` + `<h3>`):** `Your Brand Deserves to Be` / `the Answer`
- **Подзаголовок (verbatim):** `Start your 7-day free trial. Full platform access. Cancel anytime.`
- **CTA:** `Start your 7-day free trial` → `/signup`
- **Работа в аргументе:** единственное место на странице, где три снятия риска стоят рядом: срок, полнота доступа, отмена.

### 1.14 Футер
- **Слоган (verbatim):** `Where brands go to win AI search.`
- **Колонки:** `Company` (Home, Pricing, Case Study, Demo) · `Product` (7 ссылок) · `AI Rank Trackers` (7 ссылок) · `Resources` (Blog, MCP, Roadmap, Affiliates)
- **Соцсети:** LinkedIn, X, YouTube, Instagram, Facebook
- **Юридическое:** `© 2026 CrowdReply, Inc. All rights reserved.` · Privacy policy · Terms of Service · Refund Policy
- **Работа в аргументе:** футер — **SEO-инструмент**, а не навигация: 14 ссылок на отдельные feature-страницы под запросы вида «ChatGPT Rank Tracker», «Perplexity Visibility Tracker». `MCP` и `Roadmap` — сигналы для технической аудитории.

---

## 2. Продающий аргумент

**Оффер.** Не «трекер», а **трекер + исполнитель**. Формулировка из мета-описания:
`The only AI search visibility platform with a built-in Engagement Engine.` Слово
`only` — прямая заявка на уникальность категории.

**Обещание / результат.** Три уровня, от абстрактного к денежному:
1. Заголовок: `Make [AI] Mention Your Brand` — упоминание.
2. Подзаголовок: `Become the brand AI recommends.` — рекомендация.
3. Финальный CTA: `Your Brand Deserves to Be the Answer` — быть ответом.
Обещание **растёт по странице**, а не повторяется.

**Механизм — есть, и он объяснён трижды.**
- Причинная цепочка в секции «Проблема»: `They pull answers from community discussions, review sites, and editorial content. The brands in those sources get recommended. The rest get ignored.`
- Механизм действия — 4 шага Engagement Engine (найти тред → написать ответ → **мы публикуем** → следить за новыми).
- Механизм ссылок: `AI models cite the sources that real publications link to. Backlinks and brand mentions build the footprint those citations draw from.`
Это редкость: лендинг **не прячет** самую спорную часть механики (за вас пишут
комментарии с чужих аккаунтов), а делает её главным аргументом.

**Доказательства.** Рейтинг G2 `4.9` со ссылкой на источник; `Trusted by 5,000+
brands`; 12 логотипов; 7 именованных кейсов со своими страницами; 4 отзыва;
4 метрики (`+47%`, `75%`, `4%`, `2X`); скриншоты продукта; видео 90 секунд.
Разбор проверяемости — §5.

**Снятие риска.** Только одно место и только словами: `Start your 7-day free
trial. Full platform access. Cancel anytime.`
- `no credit card` на странице **отсутствует** — grep даёт **0 совпадений**.
- `guarantee` / `money-back` на странице **отсутствуют** — grep даёт **0**.
  (Сторонние обзоры упоминают 30-дневную гарантию возврата — см. §11, на самом
  лендинге её нет; в футере есть только ссылка `Refund Policy`.)
- Формы на странице нет вообще: `<form>` — **0**, `<input>` — **0**.

**Срочность / дефицит.** Практически отсутствуют. Единственный намёк — таймовые
формулировки, а не дедлайны: `Backlinks Marketplace is live`, `Listen Before AI
Does`, `Be the first to show up in conversations your competitors haven't seen
yet`, `Ordered in minutes, not months`. **Ни одного счётчика, ни одной
ограниченной по времени скидки, ни «осталось N мест».** Дефицит здесь
конкурентный («вас обойдут»), а не искусственный.

**Враг.** Врагов **два**, и это главная структурная находка:
1. *Внешний* — Google и старый SEO: `AI is the new search engine. Are you visible?`
   `ChatGPT, Perplexity, Gemini and others are replacing Google for buying decisions.`
2. *Категорийный* — остальные AEO-трекеры: `Other tools show you where you're
   missing. CrowdReply gets you in.` — одиннадцать слов, которые делают всю
   дифференциацию.

---

## 3. Позиционирование и месседжинг

**Категория.** Заявлена в титуле и в H1 буквально: `AI Search Visibility Tool`,
с префиксом `#1`. Категория молодая, поэтому её называют, а не намекают на неё.

**Против какой альтернативы.** Прямо — против **пассивных трекеров видимости**
(`Other tools show you where you're missing`). Косвенно — против платной рекламы,
через отзывы: `ranking on LLM's have driven more traffic than paid ads for us`,
`I've never seen such huge ROAS anywhere else`. Реклама не названа врагом в
копирайтинге, но подставлена в отзывы — приём чистый: сравнение делает клиент, а
не бренд.

**Before / after.**
- *Before* (verbatim): `The rest get ignored.`
- *After* (verbatim): `Become the brand AI recommends.` → `Your Brand Deserves to Be the Answer`
Картина «до» занимает ровно четыре предложения в одной секции; «после» размазано
по всей странице как повторяющееся обещание. Асимметрия намеренная: боль
проговаривается один раз и жёстко, выигрыш — многократно.

**Кому адресовано явно.** Брендам с покупательской категорией в B2B/SaaS — по
промптам-примерам: `Best CRM for B2B companies?`, `Top alternatives to HubSpot`,
`What payroll tool do startups use?`. Плюс **агентствам** — дважды:
`Shareable reports for stakeholders and clients` и отзыв `we're able to give our
clients … now we're also able to offer AI visibility to our clients`.

**Кому не адресовано.** Нет ни одного упоминания enterprise-закупки в привычном
смысле — ни SOC 2, ни SSO, ни «talk to sales» (кнопка называется `Book a demo`).
Нет упоминания локальных языков и рынков (нет `hreflang`). Нет самообслуживания
для соло-фрилансера — минимальный тариф $99/mo.

**Уровень осведомлённости первого экрана.** Рассчитан на **problem-aware /
solution-aware**, не на unaware. Доказательство: заголовок `Make [ChatGPT,
Gemini, Perplexity, Claude] Mention Your Brand` работает только на том, кто уже
знает, что ИИ-ассистенты рекомендуют бренды и что это важно. Для unaware
страница честно ставит секцию «Проблема» **вторым экраном** — то есть unaware
не отсекается, а догоняется на втором шаге. Это грамотный компромисс: первый
экран говорит с горячими, второй подхватывает холодных.

---

## 4. Копирайтинг: конкретные приёмы

### 4.1 Формула заголовка

**H1 (технический, он же бейдж):** `#1 AI Search Visibility Tool` — 28 символов,
5 слов. Формула: `[ранг] + [категория]`. Никакой выгоды, чистая
категоризация + притязание на лидерство.

**Визуальный заголовок (два `<h2>` + иконки):** `Make` ⟨ChatGPT · Gemini ·
Perplexity · Claude⟩ `Mention Your Brand` — 23 символа текста, 4 слова.
Разбор по частям:
| Часть | Verbatim | Функция |
|---|---|---|
| Глагол | `Make` | повелительное наклонение, читатель — субъект действия |
| Объект | *(иконки моделей вместо слов)* | называет всех конкурентов-ИИ разом, не тратя ни одного слова и не устаревая при появлении новой модели |
| Действие | `Mention` | конкретное, измеримое, не «grow» и не «boost» |
| Бенефициар | `Your Brand` | владение |

Приём с иконками решает три задачи сразу: длина заголовка не растёт от числа
моделей; список моделей обновляется правкой картинки, а не текста; читатель
мгновенно опознаёт «это про мой ChatGPT».

### 4.2 Длина заголовков (измерено)

| Заголовок | Слов | Символов |
|---|---|---|
| `Make … Mention Your Brand` | 4 | 23 |
| `Meet the Engagement Engine` | 4 | 26 |
| `Always Listening. Always First.` | 4 | 31 |
| `AI Backlinks Marketplace` | 3 | 24 |
| `Don't Take Our Word for It` | 6 | 26 |
| `Your Brand Deserves to Be the Answer` | 7 | 36 |
| `The Intelligence Layer Behind Your AI Presence` | 7 | 46 |
| `AI is the new search engine. Are you visible?` | 9 | 45 |

**Медиана — 4–6 слов.** Ни один заголовок не длиннее девяти слов. Подзаголовки
держатся в 10–16 словах (`Track your AI search visibility…` — 16 слов, 99
символов).

### 4.3 Кто субъект предложений (измерено по дедуплицированному тексту, 1090 слов)

| Слово | Вхождений |
|---|---|
| `your` | 24 |
| `brand` | 15 |
| `our` | 12 |
| `you` | 10 |
| `we` | 10 |
| `CrowdReply` | 10 |
| `AI` | 42 |

Соотношение «ты» к «мы» ≈ **34 : 22**. Субъект по умолчанию — **читатель**, в
повелительном наклонении: `Track…`, `Engage…`, `Become…`, `Make…`, `Find…`,
`Spot…`, `Skip outreach entirely`, `Add placements to your cart`.
`We` появляется ровно там, где нужно снять работу с читателя:
`We Post for You`, `We partner directly with each publisher`, `We track how AI
models see your brand`. То есть «мы» = «мы это сделаем за вас», а не «мы такие
классные».

### 4.4 Конкретика против пустоты

**Три самые конкретные формулировки (verbatim):**
1. `Buy editorial backlinks from a vetted catalog of 40,000+ publishers with real authority and traffic data on every site. Order in minutes, track every placement until the link is live.` — количество, критерий отбора, тип данных, срок, состояние на выходе.
2. `Posted through trusted community profiles on your behalf.` — восемь слов, которые честно называют самую спорную часть сервиса. Никакого эвфемизма.
3. `Not ready for always-on monitoring? Search once, find what matters, move on.` — называет возражение вслух и даёт под него режим продукта.

**Три самые пустые формулировки (verbatim):**
1. `The Intelligence Layer Behind Your AI Presence` — «intelligence layer» и «AI presence» одинаково подойдут любому SaaS в категории; заголовок ничего не обещает и ни от кого не отличает.
2. `See how teams are turning AI search gaps into competitive advantages.` — «gaps into competitive advantages» это чистый консалтинг-шум, стоящий над блоком отзывов, где ниже есть конкретный `$1M extra revenue`.
3. `Get answers to common questions here` — подзаголовок к `Frequently Asked Questions`, дословно повторяющий заголовок. Строка, которую можно удалить без потерь.

### 4.5 Использование чисел

Все числа страницы: `#1` · `40,000+` / `40k+` (издатели) · `5,000+` (бренды) ·
`4.9` (G2) · `90` (секунд видео) · `+47%` · `75%` · `4%` · `2X` · `$1M` ·
`4 months` · трафик тредов `1.1k`–`3.3k Visitors/mo`.

Приём, который стоит забрать: **числа-приманки внутри интерфейсных макетов**.
`2.3k Visitors/mo`, `3.3k Visitors/mo` — это не маркетинговые цифры, а подписи в
скриншоте продукта. Они показывают масштаб выгоды, не будучи обещанием, за
которое надо отвечать. То же с `DR 57`, `116.9K` в таблице маркетплейса.

Оборотная сторона: `+47%`, `75%`, `4%`, `2X` стоят **голыми плитками без единого
атрибута** — ни компании, ни периода, ни методики.

### 4.6 Глаголы

Доминируют короткие императивы действия: `Make`, `Track`, `Engage`, `Become`,
`Listen`, `Find`, `Surface`, `Craft`, `Post`, `Spot`, `Monitor`, `Benchmark`,
`Export`, `Skip`, `Order`, `Buy`, `Browse`, `Search`.
**Ни одного из «пустых» глаголов категории** — нет `unlock`, `empower`,
`leverage`, `elevate`, `supercharge`, `transform` (grep по всем — 0 совпадений).
Самый мягкий глагол на странице — `Meet` в `Meet the Engagement Engine`.

### 4.7 Надписи кнопок (все verbatim, с повторами)

| Надпись | Куда | Сколько раз (после дедупликации брейкпоинтов) |
|---|---|---|
| `Browse Catalogue` | `/features/backlinks-marketplace` | 1 (в announcement bar) |
| `Login` | `/login` | 1 |
| `Book a demo` | `/demo` | 1 |
| `Start 7 day free trial` | `/signup` | 1 |
| `Get started` | `/signup` | 1 |
| `Start Ordering` | `/signup` | 1 |
| `Start your 7-day free trial` | `/signup` | 1 |
| `Submit comment` | — | 1 (декоративная, внутри макета) |

**Дефект, который нужно вынести в наш скилл:** одно и то же действие — начать
триал — названо на сайте **тремя разными способами**:
- `Start 7 day free trial` (hero, лендинг)
- `Start your 7-day free trial` (финальный CTA, лендинг)
- `Start 7 days free trial` (тариф Starter на `/pricing`)
Три написания числительного (`7 day` / `7-day` / `7 days`) в трёх местах одного
сайта. Плюс на `/pricing` соседние тарифы зовут то же действие `Get Started`.
Это ровно то, что наш brand-hard-rule формулирует как «одно действие — одно имя».

### 4.8 Микрокопия под CTA

Есть **ровно в одном месте** — под финальным CTA: `Start your 7-day free trial.
Full platform access. Cancel anytime.` Три предложения, три снятия риска.
**Под hero-кнопками микрокопии нет вообще** — самое дорогое место страницы
работает без единой строки, снимающей страх. Это первое, что сломает A/B-тест
(см. §9).

### 4.9 Тон

Уверенный, короткий, слегка агрессивный к конкурентам, без юмора и без
самоиронии. Восклицательных знаков во всём копирайтинге — **2**, и оба внутри
цитаты клиента (`it's our best marketing channel!!`), то есть не в голосе бренда.
Эмодзи — **1** (`✨` в `CrowdReply in 90 Seconds ✨`), в нейтральном контексте.
Ни одного эмодзи и восклицания на платёжных, ошибочных или юридических
поверхностях. По нашей шкале — чистая работа.

### 4.10 Признаки машинной генерации

Померено по дедуплицированному тексту (1090 слов):

| Маркер | Найдено | Комментарий |
|---|---|---|
| `unlock`, `seamlessly`, `revolutionize`, `elevate`, `empower`, `supercharge`, `game-changing`, `effortless`, `leverage`, `cutting-edge`, `harness`, `transform`, `in today's … landscape`, `robust`, `delve` | **0** | ни одного стандартного LLM-слова |
| Тире `—` | **3** | все три перечислены ниже |
| Точка после заголовка | **0** | точки есть только *внутри* составных заголовков (`Always Listening. Always First.`, `AI is the new search engine. Are you visible?`) — это стаккато, а не хвостовая точка |
| Списки из трёх | **6** | ниже |

**Все три тире (verbatim):**
1. `See which sources AI cites — and where you're missing.` — риторическое, заменяемо запятой. **Единственный настоящий AI-tell на странице.**
2. `Surface threads across Reddit, Quora, Wikipedia, and blog sites — filtered by relevance and AI citation potential.` — приложение, тире оправдано.
3. `…give you the tools to engage on those platforms — so your brand becomes the one AI recommends.` — следствие; здесь по смыслу просится двоеточие.

**Списки из трёх (rule of three), verbatim:**
`Track your AI search visibility. Engage where AI pulls its answers. Become the
brand AI recommends.` · `helps brands monitor, engage, and grow` · `analytics,
social listening, and our proprietary Engagement Engine` · `authority, traffic,
and spam checks` · `community discussions, review sites, and editorial content` ·
`visibility trends, citation data, and engagement ROI`.
Шесть троек на 1090 слов — плотно, но у человеческого B2B-копирайтинга это тоже
норма; сама по себе тройка не улика.

**Вывод по машинности:** страница **написана заметно чище среднего** SaaS-лендинга
2026 года. Один риторический дефис, ноль buzzword-глаголов, ноль точек после
заголовков. Слабое место не в стилистике, а в **абстракции двух заголовков**
(§4.4).

---

## 5. Доказательства и доверие

### Проверяемое

| Элемент | Verbatim / данные | Почему проверяемо |
|---|---|---|
| Рейтинг G2 | `4.9` со звёздами | обёрнут в `<a href="https://www.g2.com/products/crowdreply/reviews">` — ведёт на внешний независимый источник. Само значение на G2 **не проверено** (страницу не открывал) |
| Кейсы | 7 названных компаний: `respeecher`, `stingrai`, `safegraph`, `pabau`, `lido`, `taxdome`, `lemlist` | у каждой отдельная страница `./casestudy/<name>`; компании реальные и гуглящиеся |
| Логотипы | `Xbert intelligence`, `wodify`, `Stripo`, `Omio`, `NP Digital`, `Levanta`, `Kamatera`, `instantly`, `figr`, `facetune`, `Creatio`, `Alvao` | реальные названия в `alt`; связь с продуктом **не проверена** (клиенты или просто логотипы — по странице не установить) |
| Юрлицо | `Organization` schema: `legalName: CrowdReply`, `foundingDate: 2025`, адрес `440 North Barrance Ave #8595, Covina, California, 91723`, основатели `Dawood Khan`, `Jim Løining`, `Sheryar Khan`, `sameAs` → X, LinkedIn, Facebook, Crunchbase | JSON-LD в `bodyEnd`; **основатели названы поимённо** — редкий и сильный сигнал для молодого продукта |
| Скриншоты продукта | таблица маркетплейса с `retrododo.com` (DR 57, 116.9K), `hotair.com` (DR 72, 50.4K), `Page 2 of 16`; дашборд `LLM Visibility Score & Ranking`, `10%`, `↑0.48% vs previous day`, `#8 Your rank` | это реальный UI с непричёсанными числами (`10%`, `#8` — скромные значения, не витринные) |

### Декоративное / непроверяемое

| Элемент | Verbatim | Проблема |
|---|---|---|
| Количество клиентов | `Trusted by 5,000+ brands` | нет источника, нет даты, нет определения «brand» |
| Издатели | `40,000+ vetted publishers` | заявлено четырежды на странице, ни разу не подтверждено; каталог за `/signup` и в `robots.txt` стоит `Disallow: /backlinks-marketplace` |
| Метрика 1 | `Increased LLM visibility +47%` | нет компании, периода, базы сравнения, методики |
| Метрика 2 | `Citations coverage 75%` | то же; «75% чего от чего» не определено |
| Метрика 3 | `Share of voice 4%` | 4% — само по себе не выглядит как достижение без контекста |
| Метрика 4 | `2X Increased sales` | нет привязки ни к одному кейсу |
| Отзыв 1 | `Marcus A`, `eCom` | фамилия сокращена до буквы, «компания» = категория рынка. Внутри — самое сильное число страницы: `over $1M extra revenue since January` — и оно **никак не подтверждено** |
| Отзыв 2 | `Michal H`, `Red-engage` | компания названа, но без ссылки. В тексте грамматическая ошибка: `We're been with CrowdReply since they started` |
| Отзыв 3 | `Adrina W`, `App` | «App» вместо названия компании — по сути анонимный отзыв |
| Отзыв 4 | `Patrick`, `Optimal Bet` | только имя; компания названа |
| Аватары | 24 `<img alt="Avatar">` | фото есть, но имена анонимизированы — комбинация «лицо есть, имени нет» доверия почти не добавляет |
| Заявка на лидерство | `#1 AI Search Visibility Tool` — в `<title>`, в `<h1>` и в OG-тегах | ни одного рейтинга, ни одной ссылки, ни одного «по версии X» |

**Чего на странице нет вообще:** ни одного security/compliance-бейджа (SOC 2,
GDPR, ISO), ни строки о безопасности данных, ни упоминания политики площадок
(Reddit ToS) — при том, что продукт публикует контент от лица пользователя через
`trusted community profiles`. Для продукта, чья главная фича балансирует на
правилах чужих платформ, отсутствие блока «это легально и безопасно» — заметная
дыра.

---

## 6. Механика конверсии

**Сколько CTA и сколько разных надписей.** После дедупликации трёх
брейкпоинт-вариантов: **7 конверсионных CTA, 6 разных надписей** (`Browse
Catalogue`, `Book a demo`, `Start 7 day free trial`, `Get started`, `Start
Ordering`, `Start your 7-day free trial`) + `Login`. Из них **пять из семи
ведут в одну точку — `https://crowdreply.io/signup`.**

**Где первый CTA.** Технически первый кликабельный CTA — `Browse Catalogue` в
announcement bar, **над сгибом**. Основная пара (`Book a demo` + `Start 7 day
free trial`) — тоже над сгибом, в hero. Порядок в hero: демо слева, триал
справа; primary-стилем (оранжевая заливка) выделен **триал**, демо — чёрная
кнопка. То есть страница толкает в self-serve, а демо оставляет как запасной путь.

**Один путь или несколько.** Четыре разных пути, и они **не конкурируют**:
1. Self-serve триал → `/signup` (доминирует, 5 из 7 кнопок)
2. Демо → `/demo`
3. Маркетплейс ссылок → `/features/backlinks-marketplace` (только из баннера)
4. Цены → `/pricing` (только из навигации и футера)

**Форма.** **Формы на лендинге нет вообще.** Измерено: `<form>` — 0, `<input>` —
0. Все `<button>` (11 штук, из них 3 — декоративные `Submit comment` внутри
макета продукта) не собирают данные. Вся квалификация вынесена на `/signup`,
который **закрыт от индексации** (`robots.txt`: `Disallow: /signup`).

**Трение.**
- Регистрация стоит **до** любой ценности: каталог издателей замазан блюром
  прямо на скриншоте, цены на плитках маркетплейса затёрты, `Disallow:
  /backlinks-marketplace` в robots — то есть посмотреть каталог без аккаунта
  нельзя в принципе.
- Требуется ли карта для триала — **не проверено** (страница `/signup` не
  открывалась; на лендинге строки `no credit card` нет — grep 0 совпадений).
- Блок `See your AI Visibility Score` в hero выглядит как поле ввода домена
  (`data-framer-name="Input"`), но `<input>` в SSR-HTML нет; работает ли он как
  интерактивный лид-магнит — **не проверено**.

**Как показаны цены.** **На лендинге цен нет ни одной.** Ближайшее упоминание —
вопрос FAQ `How much does CrowdReply cost?`, чей ответ в HTML отсутствует.
Реальные цены живут на `/pricing`:

| Тариф | Цена | Бренды | Промпты | Кредиты | Модели | Комментарий / тред |
|---|---|---|---|---|---|---|
| Starter | `$99` / mo | 1 | 20 | `$50 monthly credits included` | `Choose 2 models` | `$10` / `$25` |
| Growth (`Most Popular`) | `$299` / mo | 3 | 75 | `$200 monthly credits included` | `Choose 4 models` | `$8` / `$20` |
| Enterprise | `from $499` / mo | 10 | 200 | `$300 monthly credits included` | `All 7 models` | `$7` / `$15` |

Заголовок `/pricing`: `Simple Plans. Real Results.` Мета-описание там же:
`Flexible plans starting at $99/mo. Every plan includes AI search tracking,
social listening, and engagement credits. Start your 7-day free trial today.`
Отдельная секция объясняет кредиты: `Credits That Turn Insights Into
Placements` → `Persona-Based Engagement`, `Scale With Your Plan`, `Shared Across
Brands`.

**Вторичные пути.** Блог (`/blog/`, отдельный sitemap), `MCP` (`/mcp`),
`Roadmap` (`/roadmap/`), `Affiliates`, 14 feature-страниц в футере, 7 кейсов.
Сообщества/Discord нет.

**Sticky-элементы.** Шапка (плавающая pill, остаётся сверху) и **чат Crisp** —
круглый лаунчер в правом нижнем углу, виден на всех скриншотах на всех глубинах
скролла. Announcement bar — **не** sticky, уезжает вверх.

**Exit-intent.** Не обнаружен: ни одного скрипта попапа, никаких
`beforeunload`/`mouseleave`-обработчиков в SSR-HTML. **Не проверено**
исчерпывающе — модалка могла бы прийти из GTM.

---

## 7. Визуал и движение

**Тип визуала.** Гибрид, в равных долях:
1. **Настоящие скриншоты продукта** — тёмные интерфейсы на светлых карточках.
   С не-витринными числами (`10%` видимости, `#8 Your rank`) — это добавляет
   правдоподобия сильнее, чем нарисованные «95%».
2. **Абстрактные диаграммы связей** — hero: логотипы Reddit/Quora/LinkedIn/
   Wikipedia/Facebook/Instagram по краям, закруглённые линии к центру; Engagement
   Engine: узел `Your Brand` с расходящимися связями.
3. **UI-обломки как иллюстрации** — карточки-промпты с иконками моделей,
   плитки тредов с `2.3k Visitors/mo`.

**Демо продукта в действии.** Есть, но **отложенное**: карточка `CrowdReply in
90 Seconds ✨` с подписью `Click on the video thumbnail to view.` Видео не
встроено — грузится по клику. Хорошо для скорости, плохо для конверсии: тот, кто
не кликнул, видео не увидел, а автоплей без звука в 2026-м стоит дешевле.

**Анимации и скролл-эффекты.** Измерено по HTML:
- **68 элементов** отрендерены как `opacity:0;transform:translateY(50px)` —
  классический Framer «appear on scroll»: блок появляется снизу вверх с
  проявлением.
- **59 вхождений** `will-change:transform` — GPU-подготовка.
- **20 вхождений** `ticker` — бегущие карусели (логотипы, кейсы, промпты).
- `data-framer-appear-id` — Framer-механика отложенного появления.
- Продуктовые карточки под hero собраны как **раскрывающаяся стопка**
  (accordion-stack): при скролле карточки расходятся.

**Деградируют ли анимации.** `prefers-reduced-motion` встречается в CSS
**1 раз** — то есть Framer выдаёт свой стандартный минимум, а не осознанную
доступную деградацию. **Не проверено**, покрывает ли это правило все 68
appear-анимаций; учитывая, что они управляются JS, а не CSS-переходами — скорее
всего нет.

**Наблюдённая проблема ритма.** На двух из четырёх скриншотов при скролле
экран **полностью пуст** — только фоновая сетка и чат-виджет. Секции разделены
вертикальными пустотами больше одного вьюпорта, и содержимое проявляется только
по достижении триггера. Для быстро листающего пользователя это выглядит как
«страница кончилась». Это не догадка — это то, что видно на снятых кадрах.

**Ритм плотности.** Чередование выдержано: плотная секция (Engagement Engine,
4 шага + 12 плиток тредов) → разрежённая (Social Listening, 4 короткие карточки)
→ плотная (отзывы + 4 метрики) → разрежённая (FAQ) → одноэкранный финальный CTA.
Портит ритм только избыточный воздух между секциями (выше).

**Тема.** **Светлая, одна.** Кремово-белый фон (визуально ≈ `#FAFAF8`), чёрный
текст, оранжевый акцент. Ключевой токен акцента виден в градиенте H1:
`linear-gradient(0deg, rgb(249, 111, 75) 31%, rgb(130, 167, 248) 68%)` — оранжевый
`rgb(249,111,75)` в паре с голубым `rgb(130,167,248)`. Тёмная тема используется
**инверсно и точечно**: только внутри продуктовых скриншотов и на кнопке
`Book a demo`. Приём хороший — тёмные карточки читаются как «продукт», светлый
фон как «сайт».

**Типографика.** Заголовки — **Outfit** (геометрический гротеск,
`--font-selector:RlM7T3V0Zml0LXJlZ3VsYXI=`), очень плотный трекинг
(`--framer-letter-spacing:-0.02em`). Текст — `Inter Tight`. Моноширинный
`DM Mono` — для чисел и технических подписей. Три гарнитуры с ясным разделением
ролей — дисциплинированно.

---

## 8. SEO/AEO техника

**`<title>`** (verbatim, **44 символа**): `CrowdReply: The #1 AI Search
Visibility Tool` — бренд впереди, ключ сзади, `#1` как приманка для CTR. В
пределах отображаемой длины.

**`<meta name="description">`** (verbatim, **156 символов**): `The only AI search
visibility platform with a built-in Engagement Engine. Track rankings, monitor
cited conversations and place your brand where it matters.` — 156 символов, ровно
в границе усечения. Содержит дифференциатор (`The only … built-in Engagement
Engine`) и три глагола.

**H1** (verbatim, **28 символов**): `#1 AI Search Visibility Tool`.
**Дефект:** единственный `<h1>` на странице — это **бейдж-плашка над
заголовком, обёрнутая в ссылку на главную** (`<a href="./">`). Визуальный
заголовок `Make … Mention Your Brand` размечен как `<h2>`. Для машины страница
заявляет темой «инструмент №1», а не «сделай, чтобы ИИ упоминал твой бренд».
Для AEO это потеря: главное обещание страницы не имеет наивысшего структурного
веса.

**Иерархия заголовков — некорректна.** Фактический порядок в документе:
`h1 → h2 → h2 → h6 → h3 → h3 → h3 → h6 → h4 → h4 → h4 → h2 → h5 × 6 → h2 → h2 →
h2 → h5 × 3 → h2 → h2 → h2 → h2 → h3`.
Конкретные нарушения:
- `h6` (`See your AI Visibility Score`, `CrowdReply in 90 Seconds ✨`) стоят
  **выше** `h3`/`h4` — уровень выбран по кеглю, а не по смыслу. Это типовая
  болезнь Framer.
- `h5` использован для карточек-промптов (`Best CRM for B2B companies?`) — то
  есть **демо-контент размечен как заголовок**, причём повторён в DOM десятки
  раз из-за карусели и брейкпоинтов.
- Финальный CTA разорван между `h2` (`Your Brand Deserves to Be`) и `h3` (`the
  Answer`) — **одно предложение разрезано на два уровня заголовков**.

**Schema.org.** **Ровно один блок JSON-LD** (grep: `type="application/ld+json"`
→ 1), тип **`Organization`**, вставлен через сниппет Framer в `bodyEnd`.
Содержит `legalName`, `description`, `logo`, `email`, `foundingDate: 2025`,
трёх основателей, `PostalAddress`, `sameAs` (X, LinkedIn, Facebook, Crunchbase).

**Чего в разметке нет — и это главный AEO-провал страницы:**
- Нет **`FAQPage`** — при том, что на странице **восемь** готовых Q&A.
- Нет `SoftwareApplication` / `Product` / `Offer` — при том, что цены известны
  ($99/$299/$499) и живут на `/pricing`.
- Нет `AggregateRating` — при том, что рейтинг `4.9` на G2 показан визуально.
- Нет `BreadcrumbList`, нет `WebSite` c `SearchAction`.

**Двойной удар по FAQ.** Мало того что нет разметки — **семь из восьми ответов
физически отсутствуют в HTML**. Проверено двумя независимыми способами: дамп
FAQ-региона (21 000 символов сырого HTML) содержит только ответ на первый
вопрос, у остальных внутри аккордеона пустой `<div style="display:contents">`;
WebFetch по той же странице вернул `[Answer not provided in visible text]` для
вопросов 2–8. Для ИИ-краулера, который не исполняет JS, страница отвечает
ровно на один вопрос из восьми — и это на продукте, который **продаёт
видимость в ИИ-поиске**.

**OG / Twitter.** Полный набор: `og:type=website`, `og:title`, `og:description`,
`og:image` (`framerusercontent.com/images/nR512yu6FreJazIDqEv8ZicUow.png`),
`og:url`, `twitter:card=summary_large_image`, `twitter:title`,
`twitter:description`, `twitter:image`. OG- и Twitter-тексты **дословно
дублируют** title и description — упущенная возможность написать под соцсети
отдельный крючок.

**Canonical.** Есть: `<link rel="canonical" href="https://crowdreply.io/">`.

**Robots.** `<meta name="robots" content="max-image-preview:large">` — без
`index,follow` (по умолчанию индексируется). В `robots.txt` — 26 правил
`Disallow`, включая приватную зону (`/dashboard`, `/billing`, `/account`),
`/signup`, `/backlinks-marketplace`, `/api/`, `/_next/` и — грамотно —
**отсечение UTM- и click-id-параметров**: `Disallow: /*?utm_source=`,
`/*?gclid=`, `/*?fbclid=` и ещё пять. Это защита от дублей, которую делают
единицы.

**Sitemap.** `Sitemap: https://crowdreply.io/sitemap.xml` — индекс из **пяти**
под-карт: `static_sitemap.xml` (lastmod 2026-07-15), `marketing_sitemap.xml`
(2026-07-06), `casestudy_sitemap.xml` (2026-08-20), `cms-sitemap.xml`,
`blog/sitemap_index.xml`. Разделение по типам контента — правильная структура.

**Hreflang.** **Отсутствует** — ни одного `<link rel="alternate" hreflang>`.
Продукт одноязычный.

**Читается ли контент без JS.** **Да, почти весь** — это главное техническое
достоинство страницы. Framer выдаёт статический HTML, где присутствуют все
заголовки, подзаголовки, отзывы, метрики, названия фич и вопросы FAQ.
**Исключения:** ответы FAQ 2–8 и содержимое `/casestudy` (индекс кейсов в сыром
HTML содержит только `<h1>CrowdReply Case Studies</h1>` — карточки
подгружаются клиентом).

**Внутренние ссылки.** Сильная сторона. Из футера — **14 отдельных
feature-страниц**, каждая под свой ключ: `/features/prompt-research`,
`/features/ai-competitor-analysis`, `/features/ai-share-of-voice`,
`/features/ai-citation-analysis`, `/features/prompt-tracking`,
`/features/seo-ai-agent`, `/features/backlinks-marketplace`,
`/features/chatgpt-rank-tracker`, `/features/google-ai-overview-tracker`,
`/features/google-ai-mode-tracker`, `/features/chatgpt-visibility-tracker`,
`/features/perplexity-visibility-tracker`, `/features/gemini-visibility-tracker`,
`/features/grok-visibility-tracker`. Плюс 7 кейсов, блог, roadmap, MCP.
**Дефект:** якорные ссылки внутристраничной навигации (`Problem`, `Your
Competitive Moat`, `AI Search`, `Testimonials`, `FAQ`, `+47%`) отрендерены как
`<a href="./">` — то есть ведут на **корень сайта**, а не на якорь. Для
краулера это 20+ самоссылок с разными анкорами, включая бессмысленный анкор
`+47%`.

**Блог / ответы на вопросы.** Блог есть (`/blog/`, свой sitemap-индекс), но с
лендинга на него ведёт **только ссылка в футере** — ни одного контекстного
перехода из тела страницы. Контент-хаб не связан с продающей страницей.

**Артефакт шаблона.** В DOM остался служебный атрибут от купленного
Framer-шаблона: `data-framer-name="Does Biotix remember previous conversations?"`
(8 вхождений) — имя компонента из чужого проекта «Biotix». Безвредно для SEO,
но показывает происхождение блока FAQ.

---

## 9. Слабые места

**9.1. Единственный H1 — это плашка, а не заголовок.**
`<h1>#1 AI Search Visibility Tool</h1>` обёрнут в `<a href="./">` и стоит НАД
настоящим заголовком, который размечен как `<h2>`: `Make … Mention Your Brand`.
Страница про то, «как заставить ИИ упоминать бренд», сообщает машине, что она
про «инструмент №1». Это первое, что нужно менять.

**9.2. Семь из восьми ответов FAQ отсутствуют в HTML — на сайте про ИИ-видимость.**
Продукт, чей оффер дословно звучит `The brands in those sources get recommended.
The rest get ignored.`, сам отдаёт краулеру без JS ровно один ответ из восьми.
Плюс отсутствует `FAQPage`-разметка при восьми готовых Q&A. Это не мелочь: это
несоответствие продукта собственному лендингу, и в разговоре с их же ICP оно
работает против них.

**9.3. Плитки метрик — голые числа без атрибуции.**
`+47%` (Increased LLM visibility), `75%` (Citations coverage), `4%` (Share of
voice), `2X` (Increased sales). Ни компании, ни периода, ни методики, ни
сноски. Хуже: `4%` в качестве достижения без базы сравнения читается как
провал. Рядом, в отзыве, стоит `over $1M extra revenue since January` — тоже
без подтверждения. Скептичный B2B-покупатель дисконтирует такой блок целиком, и
заодно снижает доверие к соседним **проверяемым** кейсам.

**9.4. Отзывы анонимизированы до бесполезности.**
`Marcus A` / `eCom`, `Adrina W` / `App` — фамилия сокращена до буквы, поле
«компания» заполнено категорией рынка. Ни одной ссылки на LinkedIn, ни одного
названия продукта в двух случаях из четырёх. При этом у компании есть **семь
именованных кейсов** (`lemlist`, `taxdome`, `safegraph`, `respeecher` — узнаваемые
бренды). То есть настоящий соцпруф у них ЕСТЬ, но в блоке отзывов стоит слабый
суррогат. Плюс в отзыве №2 не вычитанная грамматика: `We're been with CrowdReply
since they started`.

**9.5. Под hero-кнопками нет микрокопии — и `no credit card` нет нигде.**
Grep по всей странице: `no credit card` → **0**, `guarantee`/`money-back` → **0**.
Единственное снятие риска (`Full platform access. Cancel anytime.`) стоит в
самом низу страницы, где его увидит меньшинство. Самое дорогое место — под
`Start 7 day free trial` в hero — работает без единого слова, снимающего страх.

**9.6. Одно действие названо тремя разными именами.**
`Start 7 day free trial` (hero) / `Start your 7-day free trial` (финальный CTA) /
`Start 7 days free trial` (тариф Starter на `/pricing`), плюс `Get Started` на
двух других тарифах и `Get started` в видео-карточке. Пять формулировок для двух
действий, ведущих на один и тот же `/signup`.

**9.7. На лендинге нет ни одной цены.**
Вопрос `How much does CrowdReply cost?` есть в FAQ — но его ответ, как и
остальные семь, в HTML отсутствует. Продукт стоит от $99/mo, то есть отсекает
значительную часть трафика; выяснить это можно только уйдя на `/pricing`. Для
self-serve-продукта с триалом сокрытие цены — трение без выигрыша.

**9.8. Пустые экраны при скролле.**
Прямое наблюдение на снятых кадрах: два скриншота из четырёх — полностью пустой
вьюпорт (фоновая сетка + чат-виджет). 68 элементов с `opacity:0` появляются
только по скролл-триггеру, а межсекционные отступы превышают высоту экрана.
Быстро листающий читатель дважды видит «конец страницы».

**9.9. Заявка `#1` ничем не подкреплена.**
Стоит в `<title>`, в `<h1>` и во всех OG-тегах. Ни рейтинга, ни ссылки, ни «по
версии». В категории, где сидят G2-рейтинги, это дешёвая заявка — и она
находится ровно в том элементе, который должен нести главное обещание.

**9.10. Ни одного слова о безопасности и легальности.**
Продукт публикует контент от лица клиента через `trusted community profiles` —
самая юридически и репутационно чувствительная механика на странице. Нет ни
блока о соответствии правилам площадок, ни бейджей, ни строки о данных. Первое
возражение корпоративного покупателя не закрыто нигде, включая FAQ.

**9.11. Внутристраничные якоря ведут на главную.**
Шесть навигационных ссылок (`Problem`, `Your Competitive Moat`, `AI Search`,
`Backlinks Marketplace`, `Social Listening`, `Testimonials`, `FAQ`, `+47%`)
размечены как `<a href="./">`. Якорная навигация не работает как навигация, а
для краулера создаёт самоссылки с мусорными анкорами.

**9.12. Заголовок `The Intelligence Layer Behind Your AI Presence`.**
Единственная секция страницы, чей заголовок можно поставить на лендинг любого
конкурента без правок. Соседние заголовки (`Meet the Engagement Engine`,
`Always Listening. Always First.`) конкретны — этот выпадает.

### Что сломается на первом же A/B-тесте

| Гипотеза | Почему почти наверняка выиграет |
|---|---|
| Микрокопия под hero-CTA: `Full platform access. Cancel anytime.` перенести из футера наверх | сейчас снятие риска физически недоступно тому, кто конвертится с первого экрана |
| H1 переназначить на `Make [AI] Mention Your Brand`, бейдж сделать `<p>` | главное обещание получит структурный вес; заодно уйдёт `<h1>` внутри `<a href="./">` |
| Развернуть первые 2–3 ответа FAQ по умолчанию + добавить `FAQPage` | восемь готовых Q&A сейчас не работают ни на человека без клика, ни на машину без JS |
| Заменить `Marcus A / eCom` на именованные логотипы кейсов (`lemlist`, `taxdome`) прямо в блоке отзывов | сильный соцпруф уже есть, но спрятан этажом выше |
| Добавить `from $99/mo` рядом с hero-CTA | либо вырастет качество лидов, либо упадёт объём — в обоих случаях данные ценнее нынешней неизвестности |
| Убрать `Book a demo` из hero, оставить один CTA | сейчас две кнопки конкурируют, при том что 5 из 7 CTA страницы всё равно ведут в `/signup` |
| Сжать межсекционные отступы вдвое | два пустых экрана при скролле — прямая утечка |

---

## 10. Переносимые приёмы

### (а) Работают именно здесь — из-за специфики продукта

**1. Логотипы вместо существительного в заголовке.**
Правило: когда объект обещания — это список известных сервисов, поставь в
заголовок их иконки вместо перечисления. Длина не растёт, список обновляется
картинкой, узнаваемость мгновенная.
*Пример:* `<h2>Make</h2>` + иконки Google/OpenAI/Perplexity/Claude +
`<h2>Mention Your Brand</h2>`.
*Границы:* работает только если логотипы узнаются за долю секунды. Для
неизвестных брендов приём превращается в шум.

**2. Диаграмма источников как hero-визуал.**
Правило: если продукт живёт на стыке чужих платформ, нарисуй эти платформы по
краям первого экрана и соедини линиями с центром. Механизм объясняется без
текста.
*Пример:* Reddit, Quora, LinkedIn, Wikipedia, Facebook, Instagram по периметру
hero, закруглённые линии к центральному блоку.
*Границы:* приём для продуктов-посредников; для standalone-инструмента даст
ложное ощущение зависимости.

**3. Названный собственный механизм с капитализацией.**
Правило: дай главной дифференцирующей функции имя собственное и обращайся с ним
как с брендом.
*Пример:* `Meet the Engagement Engine`; в `<meta description>` — `The only AI
search visibility platform with a built-in Engagement Engine`; в FAQ —
`our proprietary Engagement Engine`.
*Границы:* работает только если функции реально нет у конкурентов. Название,
навешенное на общую фичу, разоблачается за один клик по сравнению.

**4. Честно назвать самую спорную часть механики, а не эвфемизировать.**
Правило: если в продукте есть шаг, который вызывает вопросы, поставь его
отдельным пронумерованным шагом простыми словами.
*Пример:* `We Post for You` → `Posted through trusted community profiles on your
behalf.`
*Границы:* приём поднимает доверие только когда рядом закрыто возражение о
законности. Здесь оно **не** закрыто — см. §9.10. То есть половина приёма
исполнена.

**5. Числа-приманки внутри скриншотов продукта, а не в маркетинговых плитках.**
Правило: показывай размер выгоды подписями в интерфейсе — это иллюстрация, а не
обещание, за которое надо отвечать.
*Пример:* `Best CRM for startups — 2.3k Visitors/mo`, `Top project management
tools — 3.3k Visitors/mo`; в маркетплейсе `retrododo.com · DR 57 · 116.9K`.
*Границы:* числа должны быть правдоподобно скромными. `10%` видимости и `#8
Your rank` на дашборде работают именно потому, что не витринные.

### (б) Универсальные

**6. Обещание должно расти по странице, а не повторяться.**
Правило: сформулируй одно и то же обещание трижды, каждый раз на ступень выше.
*Пример:* `Make [AI] Mention Your Brand` (упоминание) → `Become the brand AI
recommends.` (рекомендация) → `Your Brand Deserves to Be the Answer` (быть
ответом).

**7. Одиннадцать слов, отделяющих тебя от всей категории.**
Правило: найди фразу, которая описывает, что делают ВСЕ конкуренты, и что
дополнительно делаешь ты. Поставь её подзаголовком к главной секции.
*Пример:* `Other tools show you where you're missing. CrowdReply gets you in.`
Это самая ценная строка на всей странице.

**8. Секция «Проблема» — четыре предложения, последнее приговор.**
Правило: врага, механизм и ставку уложи в один абзац, закончи коротким
приговором без смягчения.
*Пример:* `ChatGPT, Perplexity, Gemini and others are replacing Google for
buying decisions. They pull answers from community discussions, review sites,
and editorial content. The brands in those sources get recommended. **The rest
get ignored.**`
Приём: три длинных предложения-объяснения, четвёртое — четыре слова.

**9. Показывай запросы своей аудитории её словами.**
Правило: вместо абстрактного «ваши ключевые запросы» покажи 5–6 настоящих
формулировок из категории клиента.
*Пример:* `Best CRM for B2B companies?`, `Top alternatives to HubSpot`, `What
payroll tool do startups use?`, `Top analytics tools for ecommerce`.
Читатель подставляет свою категорию за полсекунды.

**10. Одна карточка фичи должна быть написана под сомневающегося.**
Правило: среди фич поставь одну, которая обращается к тому, кто ещё не готов
подписываться, и назови его состояние вслух.
*Пример:* `Single Search` → `Not ready for always-on monitoring? Search once,
find what matters, move on.`

**11. Порядок вопросов FAQ — это воронка возражений, а не алфавит.**
Правило: что это → зачем → как работает → покрытие → границы → **цена** →
бесплатная попытка → частичное использование.
*Пример:* точный порядок восьми вопросов CrowdReply, где `How much does
CrowdReply cost?` стоит шестым, а `Can I try CrowdReply for free?` седьмым —
ровно там, где их задаёт уже прогретый читатель.

**12. Финальный CTA: три снятия риска в трёх коротких предложениях.**
Правило: под последней кнопкой поставь срок, полноту и обратимость — по одному
предложению на каждое.
*Пример:* `Start your 7-day free trial. Full platform access. Cancel anytime.`
*Усиление, которого здесь нет:* тот же блок обязан стоять и под hero-кнопкой.

**13. Футер как SEO-карта, а не как навигация.**
Правило: разложи продукт на отдельные страницы под конкретные запросы и
перечисли их в футере колонкой с говорящими названиями.
*Пример:* колонка `AI Rank Trackers` с семью ссылками — `ChatGPT Rank Tracker`,
`Google AI Overview Tracker`, `Perplexity Visibility Tracker`, `Grok Visibility
Tracker` и т. д.

**14. Слоган в футере — последнее, что читают.**
Правило: закончи страницу одной строкой позиционирования, отдельной от всего
остального.
*Пример:* `Where brands go to win AI search.` — семь слов, ни одного глагола
действия, чистое место в голове.

**15. Отсекай UTM- и click-id-параметры в `robots.txt`.**
Правило: у любой страницы, на которую льют платный трафик, дубли по
параметрам обязаны быть закрыты.
*Пример:* `Disallow: /*?utm_source=` … `Disallow: /*?gclid=` `Disallow:
/*?fbclid=` — восемь правил подряд.

**16. Проксируй аналитику через свой домен.**
Правило: ставь endpoint аналитики на первопартийный путь — блокировщики
режут `*.posthog.com`, но не `/ingest`.
*Пример:* `posthog.init('phc_…', { api_host: '/ingest', ui_host:
'https://us.posthog.com' })`. Плюс собственный трекер на
`tracking.crowdreply.io`.

**17. Разделяй sitemap по типам контента.**
Правило: индекс-карта из нескольких под-карт с раздельными `lastmod` вместо
одного файла.
*Пример:* `static_sitemap.xml` (2026-07-15), `marketing_sitemap.xml`
(2026-07-06), `casestudy_sitemap.xml` (2026-08-20), `cms-sitemap.xml`,
`blog/sitemap_index.xml`.

**18. Тёмные скриншоты на светлом фоне.**
Правило: держи сайт в одной теме, а продукт показывай в противоположной.
Инверсия сама разделяет «где сайт» и «где продукт», без рамок и подписей.
*Пример:* кремовый фон страницы + тёмные карточки дашборда; единственная тёмная
кнопка страницы — `Book a demo`.

**19. Отложенное видео вместо встроенного плеера.**
Правило: превью + клик, с явной подписью, что это превью, и с обещанием
длительности прямо в заголовке.
*Пример:* `CrowdReply in 90 Seconds ✨` + `Click on the video thumbnail to view.`
*Оговорка:* выигрыш в скорости; проигрыш в конверсии — см. §7.

**20. Одно действие — одно имя (антипример, из которого правило и выводится).**
Правило: перед тем как назвать кнопку, найди это действие в реестре строк.
*Антипример с этого лендинга:* `Start 7 day free trial` / `Start your 7-day free
trial` / `Start 7 days free trial` / `Get Started` / `Get started` — пять
написаний для одного `/signup`.

---

## 11. Что не удалось проверить

1. **Реальный рейтинг и число отзывов на G2.** Ссылка
   `https://www.g2.com/products/crowdreply/reviews` присутствует, значение `4.9`
   показано на странице — но сама страница G2 не открывалась. Соответствие числа
   источнику — **не проверено**.
2. **Требуется ли банковская карта для 7-дневного триала.** `/signup` закрыт в
   `robots.txt`, регистрацию не проходил. На лендинге строки `no credit card`
   нет (grep — 0 совпадений), но это доказывает лишь её отсутствие в копирайтинге.
3. **30-дневная гарантия возврата.** Упоминается в сторонних обзорах, найденных
   через WebSearch. На самом лендинге отсутствует (grep по `guarantee`,
   `money-back` — 0). В футере есть ссылка `Refund Policy`, её содержимое —
   **не проверено**.
4. **Что именно грузит GTM-контейнер `GTM-NLP74GHQ`.** LinkedIn Insight,
   Reddit Pixel, Twitter/X pixel, session recording, exit-intent-попапы — всё это
   может приходить из контейнера. В SSR-HTML их нет; содержимое контейнера
   **не проверено**.
5. **Запись сессий в PostHog.** SDK умеет (`startSessionRecording` есть в списке
   методов), но в `posthog.init` не вызывается. Включение может быть на стороне
   проекта — **не проверено**.
6. **Идут ли A/B-тесты.** Отдельного инструмента нет (VWO/Optimizely — 0
   совпадений), feature flags PostHog доступны технически. Факт использования —
   **не проверено**.
7. **Интерактивность блока `See your AI Visibility Score`.** В SSR-HTML нет ни
   одного `<input>` и ни одного `<form>`; блок назван `data-framer-name="Input"`.
   Является ли он рабочим лид-магнитом (ввод домена → бесплатный отчёт) — **не
   проверено**.
8. **Содержимое ответов FAQ 2–8.** Установлено, что их нет в HTML; сами тексты
   не читал (аккордеоны не раскрывал, чтобы не провоцировать JS-диалоги).
9. **Содержимое страниц кейсов** (`/casestudy/lemlist` и шести других) и
   **`/demo`.** Оба URL скачаны (`/casestudy` — 474 602 б, `/demo` — 579 522 б),
   но разобран только индекс кейсов: в сыром HTML он содержит лишь
   `<h1>CrowdReply Case Studies</h1>`, карточки подгружаются клиентом.
   Конкретные цифры кейсов — **не проверено**.
10. **Блог.** Существование подтверждено (`/blog/` в футере, отдельный
    `blog/sitemap_index.xml`). Объём, качество и AEO-структура — **не проверено**.
11. **Полная прокрутка в браузере.** Снято 4 кадра (hero, видео-карточка +
    соцпруф, секция «Проблема», секция AI Search). Секции отзывов, FAQ и футера
    визуально **не проверены** — общая вкладка Chrome дважды перехватывалась
    сторонней сессией (уводило на `zerorank.ai` и `trycomp.ai`), после чего
    группа вкладок разрушалась. Копирайтинг этих секций взят из SSR-HTML и
    подтверждён WebFetch, поэтому текстовая часть отчёта полна; неизвестен
    только их визуальный вид.
12. **Деградация анимаций при `prefers-reduced-motion`.** Правило встречается в
    CSS 1 раз; покрывает ли оно все 68 JS-управляемых appear-анимаций —
    **не проверено**, тест с включённой системной настройкой не проводился.
13. **Мобильная версия.** Framer отдаёт три брейкпоинт-варианта в SSR; снят и
    осмотрен только десктоп (1440×900). Мобильный порядок секций и мобильные CTA
    — **не проверено**.
14. **Core Web Vitals.** HTML весит 1,09 МБ в одном документе, TTFB 0,77 с — но
    LCP/CLS/INP не измерялись, Lighthouse не запускался.

---

### Приложение: измерения одной таблицей

| Метрика | Значение | Как получено |
|---|---|---|
| Вес HTML | 1 140 808 байт | `curl -w "%{size_download}"`, `wc -c` |
| Время загрузки документа | 0,772 с | `curl -w "%{time_total}"` |
| Уникальных строк копирайтинга | 175 | дедупликация трёх брейкпоинт-вариантов |
| Слов копирайтинга | 1090 | `len(body.split())` |
| Блоков JSON-LD | 1 (`Organization`) | `grep -c 'type="application/ld+json"'` |
| `<form>` / `<input>` | 0 / 0 | grep |
| `<button>` | 11 (3 декоративных) | grep |
| Вопросов FAQ | 8 | подсчёт |
| Ответов FAQ в HTML | 1 | дамп FAQ-региона + подтверждение WebFetch |
| Уникальных надписей CTA | 6 (+ `Login`) | дедуплицированный инвентарь ссылок |
| CTA, ведущих на `/signup` | 5 из 7 | тот же инвентарь |
| Тире `—` | 3 | подсчёт по тексту |
| Восклицательных знаков | 2 (оба в цитате клиента) | подсчёт |
| Эмодзи | 1 (`✨`) | подсчёт |
| LLM-buzzwords (15 слов) | 0 | regex по списку |
| Элементов с appear-анимацией | 68 | `grep -c 'opacity:0;transform:translateY'` |
| `will-change:transform` | 59 | grep |
| `prefers-reduced-motion` | 1 | grep |
| `ticker` (карусели) | 20 | grep |
| Правил `Disallow` в robots.txt | 26 | `grep -c '^Disallow'` |
| Под-карт в sitemap-индексе | 5 | `grep -c '<loc>'` |
| Feature-страниц в футере | 14 (15 уникальных `/features/*` на всей странице — плюс `/features/citation-outreach` в навигации) | подсчёт уникальных `href` |
| Именованных кейсов | 7 | подсчёт ссылок `./casestudy/*` |
| Логотипов в соцпруфе | 12 | подсчёт по `alt` |
| Отзывов | 4 | подсчёт |
