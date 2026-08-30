# Разбор лендинга: trycomp.ai (Comp AI)

> Форензик-разбор для playbook «как строить лендинги». Каждое утверждение имеет
> квитанцию: verbatim-цитата, HTML-фрагмент или измеренное число. Всё, что не
> удалось проверить, помечено **не проверено** и вынесено в раздел 11.
> Verbatim-цитаты оставлены на языке оригинала (английский).

---

## 0. Паспорт

| Поле | Значение | Квитанция |
|---|---|---|
| URL | `https://www.trycomp.ai/` | — |
| Дата снятия | 2026-08-30, ~14:20 UTC | `date` в HTTP-ответе: `date: Sun, 30 Aug 2026 14:21:41 GMT` |
| Как снято | `curl` с UA Chrome/131 → `/tmp/comp.html`; перепроверка через WebFetch; рендер-проверка в Chrome (1 вкладка, 3 скриншота, network log), затем вкладка закрыта | — |
| SSR или CSR | **Полный SSR** (React Server Components + streaming). Вся продающая копия присутствует в сыром HTML до исполнения JS | `grep '<h1'` → `Compliance that helps you close deals.` найден в сыром ответе на позиции 28579 |
| Вес HTML | **901 235 байт** (~880 KB) одним документом | `curl -w "SIZE:%{size_download}"` → `SIZE:901235` |
| Вес: важный нюанс | Разметка страницы присутствует **дважды**: shell + streaming-копия внутри `<div hidden id="S:0">` (позиция 403169). То есть ~440 KB — дубль, отданный по проводу | `s.count('Compliance that helps you close deals') == 2`, `<body>` встречается ровно 1 раз |
| Объём видимого текста | **1 308 слов** на всей главной | подсчёт по очищенному от тегов тексту одной копии |
| Стек | Next.js (App Router, RSC, Turbopack) на Vercel | `x-powered-by: Next.js`, `server: Vercel`, чанк `turbopack-13fp6xk3gxrvd.js`, `vary: rsc, next-router-state-tree` |
| Шрифт | **TWK Lausanne**, self-hosted woff2, только 400 и 700 | сетевой лог: `/_next/static/media/TWKLausanne-400.…woff2`, `TWKLausanne-700.…woff2` |
| Аналитика / рост-тулинг | **В сыром HTML — ноль сторонних скриптов.** Grep по 30 маркерам (posthog, segment, gtag, GTM, mixpanel, amplitude, hotjar, clarity, fullstory, intercom, crisp, drift, plausible, fathom, rudderstack, vercel/analytics, koala, rb2b, clearbit, hubspot, fbq, linkedin, reddit, onetrust, cookiebot, termly…) — совпадений нет | `for k in …; do grep -oic "$k" comp.html; done` → единственное совпадение `dub`, и это `aria-label="Dub"`, логотип клиента |
| Аналитика: рендер-проверка | При живой загрузке — **38 запросов, все first-party** на `www.trycomp.ai`. Единственный «служебный» — `/api/c15t/init` | `read_network_requests` → все URL на `www.trycomp.ai`; сторонних хостов нет вовсе |
| Cookie-баннер / CMP | **c15t** (self-hosted, open-source consent manager), гео-осведомлённый | `set-cookie: c15t-region=eu; Path=/; Max-Age=86400`, запрос `GET /api/c15t/init` |
| A/B-тесты, session recording, чат-виджет, ad-пиксели | **Не обнаружены** ни в HTML, ни в сетевом логе до согласия на куки | см. выше; после нажатия «Accept» не проверялось — см. раздел 11 |
| Что за продукт | Open-source AI-платформа комплаенса: агенты сами собирают доказательства из 580+ интеграций, генерируют политики под конкретный бизнес и держат компанию «audit-ready» по SOC 2 / ISO 27001 / HIPAA / GDPR | `<meta name="description">`, JSON-LD `SoftwareApplication.description` |
| ICP | B2B SaaS-стартапы и scale-up, которым комплаенс блокирует enterprise-сделки. Уклон в dev-tools/OSS-среду виден по логотипам клиентов | 14 логотипов: `Dub, Persona, Corgi, Transloadit, Unkey, Inference, Better Auth, SST, Papermark, OpenCode, Primer, Modash, Dash Social, Assignar` (`aria-label` в порядке следования) |
| Цена на странице | **Отсутствует полностью.** На главной цены нет ни в каком виде; на `/pricing` — тоже нет числа | см. раздел 3 и 9 |
| Юрлицо | `© 2026 Bubba AI, Inc. d/b/a Comp AI. All rights reserved.` | футер, verbatim |
| Репозиторий | `github.com/trycompai/comp` — **1 909 звёзд, 400 форков, AGPL-3.0**, создан 2025-01-15, последний push 2026-08-09 | GitHub API `/repos/trycompai/comp` |

---

## 1. Карта секций (по порядку)

Секции в порядке документа. Формат: **название | H (verbatim) | подзаголовок (verbatim) | CTA (verbatim) | визуал | работа в аргументе**.

### 1. Sticky-навигация
- **Заголовок:** нет (лого «Comp AI»)
- **Элементы (verbatim, в порядке):** `Product` ▾ · `Frameworks` ▾ · `Customers` · `Pricing` · `Sign in` · `Book Demo`
- **CTA:** `Book Demo` — тёмно-зелёная заливка, единственная кнопка-solid в шапке
- **Визуал:** фиксированная панель, `bg-background/90 backdrop-blur-xl`, тонкая нижняя граница (`border-foreground/5`)
- **Работа:** два уровня намерения разведены — `Sign in` для существующих, `Book Demo` для новых. `Pricing` и `Customers` — прямые ссылки без дропдауна, то есть их считают самыми частыми вопросами.
- Квитанция: `<button>Product</button>`, `<button>Frameworks</button>`, `<a href="/case-studies">Customers</a>`, `<a href="/pricing">Pricing</a>`, `<a href="https://app.trycomp.ai">Sign in</a>`, `<a href="/demo">Book Demo</a>`

### 2. Герой
- **Эйбрау-бейдж:** `4.9/5` рядом с логотипом G2 и пятью звёздами цвета `#FF492C` (фирменный красный G2)
- **H1 (verbatim):** `Compliance that helps you close deals.`
- **Подзаголовок (verbatim):** `SOC 2, ISO 27001, HIPAA, and GDPR - automated with 580+ integrations. We get you audit-ready.`
- **CTA:** инлайн-форма — поле `Enter your work email` + кнопка `Get Started` со стрелкой
- **Под CTA:** четыре бейджа-печати: `SOC 2` (CERTIFIED), `HIPAA` (COMPLIANT), `GDPR` (COMPLIANT), `ISO 27001` (CERTIFIED)
- **Визуал:** тёмно-зелёная карточка со скруглёнными углами, врезанная в белую страницу; градиент `linear-gradient(135deg, #001A14, #002C22, #004D3A, #007A55)`; текст входит анимацией (`style="opacity:0;transform:translateY(12px)"` в SSR)
- **Работа:** сразу переводит разговор с «комплаенс» на «выручка». Обещание в H1 — не сертификат, а закрытые сделки. Подзаголовок берёт на себя всю фактуру (какие фреймворки, сколько интеграций), освобождая H1 для одного смысла.
- Квитанция: `<h1 class="text-white text-balance text-4xl …">Compliance that helps you close deals.</h1>`; `<input … placeholder="Enter your work email" name="work_email"/>`

### 3. Полоса социального доказательства (логотипы)
- **Заголовок (verbatim):** `Trusted by 1,000+ companies from startups to enterprise`
- **CTA:** нет
- **Визуал:** бегущая лента (marquee) из 14 логотипов
- **Работа:** количественная заявка (`1,000+`) плюс качественная (узнаваемые dev-tool-бренды). Подбор логотипов — сам по себе сигнал ICP: `Better Auth`, `SST`, `Unkey`, `OpenCode`, `Papermark`, `Dub` — это open-source-инфраструктура, то есть аудитория, которой аргумент «мы open source» вообще что-то говорит.
- Квитанция: `aria-label` в порядке следования — `Dub, Persona, Corgi, Transloadit, Unkey, Inference, Better Auth, SST, Papermark, OpenCode, Primer, Modash, Dash Social, Assignar`

### 4. «How it works» — вертикальный таймлайн на 5 шагов
- **H2 (verbatim):** `How it works`
- **Подзаголовок (verbatim):** `Automate evidence collection, policy generation, and continuous monitoring - all from a single platform.`
- **Шаги (H3 verbatim + текст verbatim):**
  1. `Pick your frameworks` — `SOC 2, ISO 27001, HIPAA, GDPR, FedRAMP - choose what you need and we handle the rest.`
  2. `Tailored to your business` — `AI learns your stack, processes, and risk tolerance to generate policies and assessments specific to you.`
  3. `Continuous evidence collection` — `Agents pull evidence from your vendors and infrastructure automatically. Risks get flagged before they become findings.`
  4. `1:1 Slack support with real experts` — `Think of us as your compliance team. Our in-house experts respond in under 3 minutes - no tickets, no email chains.`
  5. `Share a live trust center` — `Give prospects your real compliance status upfront. No back and forth, no security review bottlenecks.`
- **CTA в конце секции:** вторая инлайн-форма `Enter your work email` + `Get Started`
- **Визуал (проверено скриншотом):** нумерованные кружки 1–5, соединённые тонкой линией; текст слева, реальный UI продукта справа. Шаг 1 — панель `Frameworks` с прогресс-барами: `SOC 2 TYPE I — 92%`, `ISO 27001 — 35%`, `HIPAA — 50%`, `GDPR — 35%`. Шаг 2 — эффект печатающегося текста с курсором. Шаг 3 — граф интеграций (видны логотипы Auth0, OpenAI). Шаг 4 — мок Slack-канала `#comp-ai-cx` с реальными таймстемпами: `Tom W. 2:34 PM` → `Comp AI Support 2:35 PM`. Шаг 5 — trust center.
- **Работа:** снимает главное возражение «это долго и на нас». Шаг 4 — самый сильный ход всей страницы: заявление `respond in under 3 minutes` доказывается артефактом с таймстемпами (2:34 → 2:35 = одна минута), а не повторением цифры.

### 5. «Compliance for every stage of growth» — сегментация табами
- **H2 (verbatim):** `Compliance for every stage of growth`
- **Подзаголовок (verbatim):** `Scales with you from seed-stage startup to global enterprise, from your first framework to full regulatory governance.`
- **Табы (verbatim):** `01 Startup` · `02 Mid-Market` · `03 Enterprise`
- **Startup:** `Close your first enterprise deals faster. Get audit-ready with AI-powered automation.` — буллеты: `SOC 2 Type I & II audit-ready in days, not weeks or months` / `AI-first compliance, so you can focus on building` / `1:1 Slack support, with real compliance experts`
- **Mid-Market:** `Scale compliance as your team and customer base grow without adding headcount.` — буллеты: `Support for custom frameworks` / `580+ real-world integrations` / `Priority onboarding and live support`
- **Enterprise:** `Handles complexity at scale. From FedRAMP to any other framework, meet the most demanding regulatory requirements.` — буллеты: `Custom control mapping across frameworks` / `Fully managed self-hosting` / `Dedicated compliance team with 99.9% uptime SLA`
- **CTA:** `Book Demo` в каждом табе (3 штуки)
- **Работа:** заменяет прайс-таблицу. Читатель самоидентифицируется по размеру компании и получает свой набор аргументов — но **без цены**, поэтому единственный выход из секции — звонок.
- **Техническая деталь:** в SSR отрендерен только активный таб (`Startup`); буллеты Mid-Market и Enterprise появляются лишь после гидратации. Проверено: SSR-извлечение показало три буллета, `get_page_text` после JS — девять.

### 6. Отзывы
- **H2 (verbatim):** `Trusted by teams who ship fast`
- **Подзаголовок (verbatim):** `Compliance shouldn't slow down your business or halt growth.`
- **CTA в конце:** третья форма `Enter your work email` + `Get Started`
- **6 отзывов, все именные, с должностью и компанией, с фото:**
  1. **Daniel Rascon, CTO, Persona AI** — `We were maybe 30-40% of the way through with Vanta when we switched to Comp AI. In less than 2 weeks, we had everything in order to start our SOC 2 Type II observation period.`
  2. **Nathan Broadbent, CEO, Docspring** — `Comp AI has been great for us. The platform is simple to use, which takes a lot of the stress out of SOC 2. Their new AI features handle a bunch of the tedious work in the background, so the whole process feels lighter.`
  3. **Glenn E., CEO, Luthor AI** — `Comp AI is like hiring an extremely talented compliance team that works day and night to help you get compliant. …`
  4. **Martin Donadieu, Founder, Capgo** — `If you want a solid compliance solution without wasting any time, just go with Comp AI. …`
  5. **Julien Monguillot, Founder, ShiftControl** — `ShiftControl is a B2B product with extremely sensitive admin access - compliance for us wasn't an option, it was essential. …`
  6. **Jana D., SessionLab** — `Comp AI was very helpful throughout. They were responsive, clear, and proactive, …`
- **Визуал / квитанция подлинности:** аватары грузятся с **Slack CDN**, а не из папки с картинками: `src=/_next/image?url=https%3A%2F%2Fca.slack-edge.com%2FT0702R613HQ-U0851S58RL3-…`. Все шесть — `ca.slack-edge.com`. Это буквально фото людей из общих Slack-каналов поддержки.
- **Работа:** отзыв №1 — единственное место на главной, где конкурент назван по имени. Он делает работу целой сравнительной секции: `30-40% of the way through with Vanta` → `In less than 2 weeks` у нас.

### 7. «The AI-first compliance platform» — сетка возможностей
- **H2 (verbatim):** `The AI-first compliance platform`
- **Подзаголовок (verbatim):** `Automate evidence collection, policy generation, and continuous monitoring - all from a single platform.` (**дословный повтор подзаголовка секции 4**)
- **5 карточек (H3 verbatim + текст verbatim):**
  - `Automated evidence collection` — `Screenshots, policies, and system checks - collected and validated automatically.`
  - `Vendor & risk monitoring` — `Risk scoring, vendor management, and alerts - before issues become audit findings.`
  - `Device agents` — `Open-source agent that monitors encryption, firewall, and security settings on every device 24/7.`
  - `Penetration testing` — `Agents probe your code, APIs, and infrastructure. Get audit-ready reports automatically.`
  - `Cloud monitoring` — `Daily scans of your cloud infrastructure so you can focus on building.`
- **CTA:** четвёртая форма `Get Started`
- **Визуал:** пять реальных скриншотов продукта (`/features/evidence_collection.webp`, `vendor_risk_monitoring.webp`, `device_agent.webp`, `penetration_tests.webp`, `cloud_monitoring.webp`), качество `q=100`, ширина до `3840`
- **Работа:** переводит разговор из «что вы делаете» в «что вы уже построили». `Penetration testing` здесь — не фича, а удар по цене конкурента: пентест у Vanta/Drata покупается отдельно.

### 8. Интеграции
- **H2 (verbatim):** `Connect with your existing stack`
- **Подзаголовок (verbatim):** `Integrates with 580+ tools out of the box to automatically collect evidence and keep you compliant.`
- **CTA:** нет
- **Визуал:** 3D-наклонённая (`rotate-x-6 hover:rotate-x-0`) бегущая сетка иконок с радиальной маской затухания по краям; ~37 инлайн-SVG
- **Работа:** превращает абстрактное число `580+` в визуальную плотность. Логотипы декоративны: контейнеры помечены `aria-hidden="true"`, ни одного названия в дереве доступности.

### 9. «Compliance that actually improves your security» — 6 пронумерованных аргументов
- **H2 (verbatim):** `Compliance that actually improves your security`
- **Подзаголовок (verbatim):** `Most platforms give you a checklist. We give you a security posture you can prove - continuously, automatically, and in the open.`
- **Шесть блоков (verbatim), каждый построен как «У всех остальных X → у нас Y»:**
  1. `01. Evidence that's never stale` — `Most platforms rely on manual screenshots and spreadsheets. By the time you collect evidence, something has already regressed. We pull evidence continuously from 580+ integrations - every config, every screenshot, every log - so your compliance posture reflects reality, not last quarter.` → ссылка `Integration platform on GitHub ↗`
  2. `02. Policies written for your business, not a template` — `Other platforms hand you generic policy documents and call it done. We generate every policy from the context you provide during onboarding - your stack, your processes, your risk tolerance. No two customers get the same boilerplate.`
  3. `03. A device agent that never sleeps` — `A checklist doesn't stop a misconfigured laptop at 2am. Our open-source device agent runs 24/7 on every employee machine - checking disk encryption, firewall status, screen lock, password length, and antivirus. Failures are flagged instantly, not discovered during the next audit cycle.` → `Device agent on GitHub ↗`
  4. `04. Automated tests you can write yourself` — `Say "show me that SSL is active on my domain" and it generates an automated test that runs daily. Or give it browser instructions - "go to our GitHub repo, click settings, verify branch protection rules" - and AI opens a browser, verifies the control, and screenshots the result. Every evidence piece is auditable and logged.`
  5. `05. Trust portals that reflect reality` — `Most trust centers are static marketing pages. Ours is live-monitored - only published policies appear, and only verified controls are shown. The moment a policy is marked as draft or a control fails, it's removed automatically. What your customers see is what you actually have.` → `View ours ↗` (ведёт на `https://security.trycomp.ai`)
  6. `06. Open source and verifiable` — `Most compliance platforms are black boxes - you trust them because you have to. We're fully open source. Every agent, every integration, every check is auditable on GitHub. You don't take our word for it, you verify it.` → `View the full source on GitHub ↗`
- **CTA:** пятая форма `Get Started`
- **Работа:** **смысловой центр лендинга.** Здесь и только здесь появляется враг — «остальные платформы» — и здесь же выдаются проверяемые ссылки. Три из шести блоков заканчиваются не кнопкой, а внешней ссылкой, по которой утверждение можно проверить самому. Это единственный на странице механизм, который отдаёт трафик наружу — и он же самый сильный.

### 10. FAQ
- **H2 (verbatim):** `Frequently Asked Questions`
- **Подзаголовок (verbatim):** `Everything you need to know about Comp AI and how it works.`
- **Три категории-таба (H3):** `Platform` · `How It Works` · `Auditing`
- **7 вопросов (verbatim):** `What is Comp AI?` / `Is Comp AI open source?` / `How does evidence collection work?` / `How are policies generated?` / `How long does it take to get audit-ready?` / `Can I bring my own auditor?` / `Does Comp AI generate the audit report?`
- **CTA:** шестая форма `Get Started`
- **Критическая техническая деталь:** **ответы отсутствуют в DOM — и до, и после гидратации.** Они существуют только внутри `<script type="application/ld+json">`. Проверено дважды: (а) после удаления всех ld+json-блоков из HTML строка `auditor-agnostic` не встречается ни разу в разметке — все 3 вхождения помечены `in_script=True`; (б) `get_page_text` в живом браузере после полной гидратации вернул только вопросы, без единого ответа.
- **Работа:** обслуживает два разных читателя разными каналами. Поисковик и LLM получают полный FAQ через schema.org; человек — только заголовки, пока не кликнет.

### 11. Финальный CTA
- **H2 (verbatim):** `Don't let compliance slow down your pipeline`
- **Подзаголовок (verbatim):** `AI agents automate the busywork - evidence collection, monitoring, audit prep - so your team can focus on closing deals.`
- **CTA:** седьмая форма `Enter your work email` + `Get Started`
- **Работа:** замыкает кольцо с H1. Открылись на `close deals` — закрылись на `closing deals`. Формулировка сменила модальность с позитивной («поможет закрывать») на негативную («не дай затормозить пайплайн») — та же мысль, другой рычаг.

### 12. Футер
- **Дескриптор (verbatim):** `AI-powered compliance platform. Get SOC 2, ISO 27001, HIPAA and GDPR audit-ready in record time.`
- **Два физических адреса:** `HQ — 2999 NE 191st Street, Suite 500, Aventura, Florida 33180`; `Mailing — 2261 Market Street, San Francisco, CA 94114`
- **Колонки:** `Product` (How it works, Platform, Book a Demo) · `Resources` (Case Studies, Compliance Hub, Tools & Templates, Documentation, Trust Center, Security, GitHub, Press, Careers, Partnerships) · `Guides` (SOC 2 Cost, SOC 2 Checklist, SOC 2 for Startups, SOC 1 vs SOC 2, ISO 42001, GRC Automation) · `Compare` (Vanta Pricing, Drata Pricing, Secureframe Pricing, Drata vs Vanta, Vanta Competitors, Drata Competitors) · `Legal` (Legal Overview, Terms, Privacy, Cookies, DPA, SLA, Subprocessors)
- **Внизу:** повтор четырёх печатей (ISO 27001, SOC 2, HIPAA, GDPR), соцсети (GitHub, X/Twitter, LinkedIn, YouTube), `© 2026 Bubba AI, Inc. d/b/a Comp AI. All rights reserved.`, и живой статус-индикатор `All Systems Normal` со ссылкой на `https://status.trycomp.ai`
- **Работа:** футер несёт два отдельных боевых блока. `Compare` — SEO-плацдарм против инкумбентов (6 страниц, ни одна не про себя). `Legal` из 7 пунктов, включая `DPA`, `SLA`, `Subprocessors` — это не юридическая гигиена, а часть продающего аргумента: продавец комплаенса, у которого нет собственного DPA, неубедителен.

---

## 2. Продающий аргумент

**Оффер.** Мы доводим вас до состояния «готов к аудиту» по SOC 2 / ISO 27001 / HIPAA / GDPR — с ИИ-агентами вместо вашей работы, с аудитом и пентестом внутри, и с исходниками, которые вы можете прочитать.

**Обещание / результат.** Не сертификат, а **выручка**. Это заявлено в H1 (`Compliance that helps you close deals.`), повторено в сегменте Startup (`Close your first enterprise deals faster`), и закрыто в финальном CTA (`Don't let compliance slow down your pipeline`). Комплаенс поставлен не как обязанность, а как узкое место в пайплайне продаж.

**Механизм.** Пять шагов из секции «How it works», каждый со своим глаголом: выбрать → адаптировать → собирать непрерывно → поддержать вживую → показать наружу. Ключевая механическая заявка — `Agents pull evidence from your vendors and infrastructure automatically. Risks get flagged before they become findings.`

**Доказательства (по убыванию проверяемости):**
1. **Проверяемое действием:** `View the full source on GitHub ↗`, `Integration platform on GitHub ↗`, `Device agent on GitHub ↗`, `View ours ↗` (собственный trust center), `All Systems Normal` (статус-страница). Пять внешних ссылок, каждая из которых позволяет проверить утверждение самостоятельно.
2. **Именное:** 6 отзывов с именем, должностью, компанией и фото из Slack CDN.
3. **Артефактное:** мок Slack-треда с таймстемпами `2:34 PM → 2:35 PM`, доказывающий `respond in under 3 minutes`.
4. **Количественное без источника:** `580+ integrations`, `1,000+ companies`, `4.9/5`, `under 3 minutes`, `24/7`, `99.9% uptime SLA` — ни у одного нет ссылки на подтверждение на самой странице.
5. **Декоративное:** лента из 14 логотипов клиентов, сетка иконок интеграций (`aria-hidden`).

**Снятие риска.** На главной — **отсутствует**. Нет ни бесплатного триала, ни гарантии возврата, ни «no credit card required», ни срока. Единственный смягчитель — `Can I bring my own auditor?` в FAQ (`Comp AI is auditor-agnostic`), то есть снятие страха вендор-лока, а не финансового риска. Настоящая работа с риском вынесена на `/demo` (`20-min call · Quote emailed after · No contract to sign`) и `/pricing` (`Money-back guarantee`) — то есть **предъявляется только тем, кто уже пошёл в воронку**.

**Срочность.** Прямой срочности нет: ни таймера, ни дедлайна, ни «осталось мест». Вместо неё — **срочность, взятая взаймы у покупателя**: подразумевается, что сделка уже висит и ждёт SOC 2. Она проговорена в кейсах (`We were told to get SOC 2 compliant by our first big customer`) и в темпе (`audit-ready in days, not weeks or months`).

**Против чего продают (враг).** Враг двухслойный и назван по-разному в двух местах:
- **На главной — обезличенно:** `Most platforms give you a checklist`, `Most compliance platforms are black boxes - you trust them because you have to`, `Other platforms hand you generic policy documents and call it done`, `Most trust centers are static marketing pages`. Пять раз «most platforms / other platforms», ни одного имени.
- **Кроме одного места:** отзыв Daniel Rascon называет Vanta прямо. Конкурент назван устами клиента, а не собственным голосом — приём, который снимает с бренда ответственность за сравнение.
- **По имени — во внешнем слое:** блок футера `Compare` (Vanta Pricing, Drata Pricing, Secureframe Pricing, Drata vs Vanta, Vanta Competitors, Drata Competitors) и `<meta name="keywords">`, где прямым текстом стоит `Vanta alternative,Drata alternative`.

Итог: **главная воюет с категорией, а посадочные страницы воюют с конкретными брендами.** Это разделение сделано сознательно.

---

## 3. Позиционирование и месседжинг

**Категория.** Заявлена трижды и по-разному:
- в `<title>`: `AI Compliance Software`
- на странице (H2): `The AI-first compliance platform`
- в JSON-LD: `The agentic compliance platform` (`Organization.description`), `applicationSubCategory: "Compliance Software"`

Расхождение неслучайно: `agentic` — слово для инвесторов и машин, `AI-first` — для покупателя, `AI Compliance Software` — для поиска.

**Альтернатива, против которой позиционируются.** Vanta и Drata, плюс Secureframe третьим. В самой странице они не названы (кроме отзыва); в служебных полях — названы прямо: `<meta name="keywords" content="…,Vanta alternative,Drata alternative">`.

**Before / after:**

| Before (жизнь без нас) | After (жизнь с нами) | Verbatim-квитанция |
|---|---|---|
| Доказательства собираются вручную и устаревают | Доказательства тянутся непрерывно | `manual screenshots and spreadsheets. By the time you collect evidence, something has already regressed` → `so your compliance posture reflects reality, not last quarter` |
| Политики — шаблон, одинаковый у всех | Политики — из вашего контекста | `generic policy documents and call it done` → `No two customers get the same boilerplate` |
| Ноутбук с плохой конфигурацией найдут на следующем аудите | Найдут мгновенно | `A checklist doesn't stop a misconfigured laptop at 2am` → `Failures are flagged instantly, not discovered during the next audit cycle` |
| Trust center — маркетинговая страница | Trust center — живое состояние | `Most trust centers are static marketing pages` → `What your customers see is what you actually have` |
| Платформа — чёрный ящик, доверяете вынужденно | Можно проверить | `you trust them because you have to` → `You don't take our word for it, you verify it` |
| Поддержка через тикеты | 1:1 в Slack за 3 минуты | `no tickets, no email chains` |
| Комплаенс тормозит сделки | Комплаенс закрывает сделки | `Don't let compliance slow down your pipeline` |

**Адресат.** Основатель или CTO стартапа/scale-up, у которого enterprise-клиент потребовал SOC 2. Признаки: сегмент `Startup` стоит первым и раскрыт по умолчанию; все отзывы — от CTO/CEO/Founder, ни одного от Compliance Manager или CISO; язык бенефита — про сделки и время инженеров, не про снижение регуляторного риска.

**Уровень осведомлённости на первом экране.** **Solution-aware, близко к product-aware.** Первый экран не объясняет, что такое SOC 2 и зачем он нужен — он сразу перечисляет аббревиатуры как известные. Читатель, который не знает, что такое ISO 27001, отваливается на подзаголовке. Это осознанная ставка: страница написана для человека, который **уже ищет платформу**, а не для того, кто впервые узнал о проблеме. Problem-aware-трафик обслуживается отдельно — страницами `/soc-2-cost`, `/soc-2-checklist`, `/soc-2-for-startups`, `/hub`.

### Open-source и прозрачность цены как оружие — асимметрия

Это самое интересное место всего разбора, потому что два «оружия прозрачности» применены **прямо противоположным образом**.

**Open-source используется как оружие — и работает.** Аргумент выстроен полностью:
- утверждение: `We're fully open source. Every agent, every integration, every check is auditable on GitHub.`
- переформулировка в эпистемическом ключе: `You don't take our word for it, you verify it.`
- удар по врагу: `Most compliance platforms are black boxes - you trust them because you have to.`
- три работающие ссылки на конкретные пакеты, а не на общий репозиторий: `/tree/main/packages/integration-platform`, `/tree/main/packages/device-agent`, и корень репозитория
- подтверждение в FAQ (schema): `Yes, 100%. You can inspect every line of code on GitHub. Full transparency, no vendor lock-in, no black boxes.`
- измеренная реальность за ссылкой: репозиторий существует, живой, AGPL-3.0, 1 909 звёзд, 400 форков, push 9 дней назад

Это не декларация, а **проверяемое обещание**, и это редкость. Ключевой риторический ход — превратить open-source из технической характеристики в **эпистемологический аргумент**: «вопрос не в том, лучше ли мы, а в том, что нас можно проверить, а их нельзя».

**Прозрачность цены НЕ используется — и это зияющая дыра в той же броне.**

На главной цены нет вообще. На `/pricing` — тоже:
- H1: `Pricing tailored to your compliance scope.`
- лид: `Compliance pricing depends on your frameworks, team size, and deadline, so we don't hide a rate card. We prepare your exact number and present it on a 20-minute call.`
- собственный FAQ-вопрос: `Why don't you publish a price list?` — ответ: `Because a flat rate would overcharge simple programs and undercharge complex ones. A 20-person startup pursuing SOC 2 and a 500-person company running SOC 2, ISO 27001, and HIPAA have very different programs. We price the program you actually need.`

При этом **цены конкурентов они публикуют охотно**. Страница `/vanta-pricing` (`<title>Vanta Pricing 2026: Complete Cost Breakdown | Comp AI`) даёт таблицу:
- `Startup — $10,000 - $20,000/year`
- `Growth — $25,000 - $50,000/year`
- `Enterprise — $50,000 - $100,000+/year`
- отдельный блок `Hidden costs / Additional costs with Vanta`: `Additional frameworks: $5,000 - $15,000 each`, `Implementation/onboarding fees: $2,000 - $10,000`, `Premium support tiers: Additional cost`, `Custom integrations: Professional services rates`
- с оговоркой: `Pricing is not publicly listed and requires a sales call. These ranges are based on market research.`
- и с контр-оффером: `Audit + pen test bundled — SOC 2 audit and penetration testing included. No surprise $10-30K costs at audit time`

**Итог асимметрии:** они атакуют конкурента за то, что его цена скрыта (`Pricing is not publicly listed and requires a sales call`), публикуют оценку его цены — и на собственной странице цен не публикуют ни одного числа, требуя тот же самый sales-call. Позиционирование «нас можно проверить» держится ровно до строки, где начинается счёт.

---

## 4. Копирайтинг: конкретные приёмы

### Формула H1

**`Compliance that helps you close deals.`** — 38 символов, 6 слов.

Разбор по частям:
| Часть | Что делает |
|---|---|
| `Compliance` | Категория первым словом. Мгновенная квалификация: не в теме — уходи. |
| `that helps you` | Связка, переопределяющая роль. Комплаенс становится **субъектом, который вам помогает**, а не обязанностью, которую вы исполняете. Инверсия отношения. |
| `close deals` | Бизнес-результат вместо продуктового. Не «получить SOC 2», не «автоматизировать комплаенс» — а метрика, за которую отвечает читатель. |
| `.` (точка) | Точка в конце H1. По нашему брендбуку это ошибка (заголовок — имя, а не утверждение). Здесь она сделана намеренно: превращает заголовок в декларацию. Отмечаю как расхождение, не как эталон. |

Формула, пригодная к переносу: **`<Категория> that <переопределённая роль> <метрика читателя>`**.
Пустой вариант той же мысли звучал бы как `The AI-native compliance automation platform` — то есть ровно то, что стоит в их же H2 секции 7. Сравнение двух формулировок в пределах одной страницы — готовый учебный пример.

### Длина заголовков

- `<title>`: 41 символ
- `<meta description>`: 134 символа (влезает в сниппет)
- H1: 38 символов / 6 слов
- Подзаголовок героя: 93 символа / 16 слов
- H2 по странице: от 13 (`How it works`) до 46 (`Compliance that actually improves your security`) символов
- Медианный H2 — около 30 символов. **Ни один H2 не длиннее одной строки на десктопе.**

### Субъект предложений

Три субъекта, распределённые по функциям, и распределение не случайно:
- **`We` — когда речь о работе и обязательстве:** `We get you audit-ready.`, `We pull evidence continuously…`, `We generate every policy…`, `We give you a security posture you can prove`, `We're fully open source.`
- **`You / your` — когда речь о выгоде и владении:** `Compliance that helps **you** close deals`, `**your** stack, **your** processes, **your** risk tolerance`, `**You** don't take our word for it, **you** verify it`, `Automated tests **you** can write yourself`
- **`Agents` / `AI` — когда речь о механизме:** `Agents pull evidence…`, `AI learns your stack…`, `Agents probe your code…`, `AI agents automate the busywork`

Продукт **почти никогда не является субъектом**. Нет «Comp AI does X» — есть «мы» и «агенты». Название бренда в теле страницы встречается всего в двух местах: в отзывах (чужой голос) и в вопросах FAQ.

### Три самые конкретные формулировки (verbatim)

1. `Say "show me that SSL is active on my domain" and it generates an automated test that runs daily. Or give it browser instructions - "go to our GitHub repo, click settings, verify branch protection rules" - and AI opens a browser, verifies the control, and screenshots the result.`
   — конкретна тем, что цитирует **вход пользователя**, а не описывает возможность. Читатель видит команду, которую сам может ввести.
2. `Our open-source device agent runs 24/7 on every employee machine - checking disk encryption, firewall status, screen lock, password length, and antivirus.`
   — пять названных проверок вместо слова «мониторинг».
3. `Our in-house experts respond in under 3 minutes - no tickets, no email chains.`
   — число + две названные вещи, которых не будет. И оно единственное подкреплено артефактом (таймстемпы в Slack-моке).

Почётное упоминание: `A checklist doesn't stop a misconfigured laptop at 2am.` — конкретна не числом, а **сценой**. Одна из немногих строк, которую читатель может увидеть.

### Три самые пустые формулировки (verbatim)

1. `The AI-first compliance platform` (H2 секции 7) — три модных слова подряд, ноль информации. Взаимозаменяемо с любым конкурентом.
2. `Scales with you from seed-stage startup to global enterprise, from your first framework to full regulatory governance.` — двойная антитеза «от … до …», означающая «мы работаем со всеми», то есть ни с кем конкретно.
3. `Automate evidence collection, policy generation, and continuous monitoring - all from a single platform.` — **и она использована дважды дословно**, как подзаголовок секции 4 и секции 7. Одна и та же строка не может быть ответом на два разных вопроса; повтор выдаёт, что её никто не перечитывал.

Ещё: `Handles complexity at scale.` — четыре слова, ни одно из которых не проверяемо.

### Числа

Все числа, встречающиеся на главной, и их статус:

| Число | Контекст (verbatim) | Проверяемо на странице? |
|---|---|---|
| `580+` | `580+ integrations` — встречается **4 раза** | Нет. Нет ссылки на каталог интеграций |
| `1,000+` | `Trusted by 1,000+ companies from startups to enterprise` | Нет |
| `4.9/5` | бейдж в герое, рядом логотип G2 | Частично: логотип G2 атрибутирует источник, но нет ни числа отзывов, ни ссылки на профиль G2 |
| `under 3 minutes` | `Our in-house experts respond in under 3 minutes` | Косвенно — через мок Slack-треда `2:34 PM → 2:35 PM` |
| `24/7` | `runs 24/7 on every employee machine` | Нет (но код агента открыт) |
| `99.9%` | `Dedicated compliance team with 99.9% uptime SLA` (только таб Enterprise) | Частично: `/legal/sla` существует |
| `2am` | `A checklist doesn't stop a misconfigured laptop at 2am` | Риторическое, не заявка |
| `1:1` | `1:1 Slack support with real experts` | Нет |
| `30-40%` | внутри отзыва Daniel Rascon | Атрибутировано человеку |
| `2 weeks` | внутри того же отзыва | Атрибутировано человеку |

**Разрыв, который стоит отметить.** Бейдж в герое показывает `4.9/5`. JSON-LD той же страницы объявляет `"aggregateRating": {"ratingValue": "4.7", "reviewCount": "64"}`. Человек видит 4.9, машина читает 4.7. Число отзывов (64) существует в разметке, но на экран не выводится — при том что 64 отзыва это как раз то, что делает 4.7 достоверным.

**Чего на главной нет ни одного:** денежной суммы, срока в днях с числом, процента экономии. Все самые сильные числа компании (`$400,000+ ARR unlocked`, `6 days to audit-ready`, `85 hours saved`) живут на `/case-studies` — на клик дальше.

### Глаголы

Доминируют глаголы действия в настоящем времени, третьим лицом от агента: `pull`, `generate`, `collect`, `monitor`, `probe`, `scan`, `flag`, `verify`, `screenshot`, `map`, `validate`, `respond`.

Отдельно стоит отметить `screenshots` как **глагол**: `AI opens a browser, verifies the control, and screenshots the result.` Превращение существительного в глагол — приём, который делает описание механическим и конкретным.

Модальных и обещательных глаголов почти нет: ни одного `can help you`, `will enable`, `allows you to`. Единственное исключение — само H1 (`helps`), и там это осознанно.

### Все надписи кнопок verbatim, с повторами

Подсчёт по одной копии разметки:

| Надпись | Раз | Где |
|---|---|---|
| `Get Started` | **7** | герой + после каждой из 6 секций; всегда submit инлайн-формы |
| `Book Demo` | **4** | шапка + по одному в каждом из трёх табов сегментации |
| `Book a Demo` | 1 | футер (**расхождение с `Book Demo` — то же действие, два имени**) |
| `Sign in` | 1 | шапка |
| `Book my pricing call` | 1 | на `/pricing`, финальный CTA |
| `Continue` / `Next` | 1 + 1 | шаг 1 формы на `/pricing` и `/demo` — **опять два имени одного шага** |
| `View all` | 1 | внутри скриншота продукта, не кликабельно |

Итого на главной **13 кликабельных CTA**, но всего **3 уникальные надписи** (`Get Started`, `Book Demo`, `Sign in`). Дисциплина высокая — с двумя нарушениями правила «одно действие — одно имя»: `Book Demo` / `Book a Demo` и `Continue` / `Next`.

Ссылки-доказательства оформлены отдельным классом надписей, все со стрелкой `↗`: `Integration platform on GitHub ↗`, `Device agent on GitHub ↗`, `View ours ↗`, `View the full source on GitHub ↗`. Визуально они не кнопки — и это правильно, они и не конверсионные.

### Микрокопия под CTA

**На главной — её нет.** Ни под одной из семи форм нет ни строки про то, что произойдёт после отправки, ни про кредитную карту, ни про приватность. Поле `Enter your work email` + кнопка `Get Started` — и всё. Это осознанный минимализм, но он оставляет читателя без ответа на вопрос «что случится, когда я нажму».

**На `/demo` микрокопия есть, и хорошая (verbatim):**
- `20-min call · Quote emailed after · No contract to sign`
- `By submitting, you agree to our Terms and Privacy Policy.`
- и целая секция `What happens on your 20-min demo` с поминутной раскладкой: `5 min — Understand your situation`, `12 min — See Comp AI solve your compliance problem`, `3 min — Fixed-fee quote + timeline`

**На `/pricing` тоже (verbatim):** `20 minutes · Pick your own time · Money-back guarantee`, `Step 1 of 3`, `Next: choose a time that works for you.`

То есть команда умеет писать микрокопию — просто не поставила её туда, где стоит семь форм.

### Тон

Уверенный, прямой, слегка конфронтационный по отношению к категории. Короткие предложения. Регулярный приём — **отрицание вместо утверждения**: `no tickets, no email chains`, `No back and forth`, `not weeks or months`, `not last quarter`, `not a template`, `no vendor lock-in, no black boxes`, `No two customers get the same boilerplate`. Читателю проще опознать себя в том, чего он не хочет.

Ни одного восклицательного знака. Ни одного эмодзи. Ни одной шутки. Для категории (комплаенс, деньги, аудит) — правильно.

### Признаки машинной генерации

**Найдено:**

1. **Риторическое тире — 20 вхождений на главной**, и это главный маркер. Причём em-dash (`—`) не использован **ни разу** (`t.count('—') == 0`); везде стоит дефис в пробелах (` - `). Примеры: `SOC 2, ISO 27001, HIPAA, and GDPR - automated with 580+ integrations`, `Screenshots, policies, and system checks - collected and validated`, `no tickets, no email chains`, `every config, every screenshot, every log - so your…`.
   Картина характерная: похоже на **пост-обработку**, где em-dash заменили на ` - ` find-and-replace'ом. Это не убирает тик, а только меняет его глиф — синтаксическая роль (тире вместо запятой, двоеточия или точки) сохранена во всех 20 случаях.
   Подтверждение гипотезы о find-and-replace: на `/demo` уцелели **3 em-dash** (`— emailed to you after the demo`), на `/pricing` — 0 тире вообще и 2 типографские апострофа (`don't`, `We'll`), которых нет на главной. Три страницы обработаны разными руками или в разное время.
2. **Триады «X, Y, and Z» — сплошным ковром.** `evidence collection, policy generation, and continuous monitoring`; `your stack, processes, and risk tolerance`; `Screenshots, policies, and system checks`; `Risk scoring, vendor management, and alerts`; `encryption, firewall, and security settings`; `your code, APIs, and infrastructure`; `organized evidence, controls, and policies`. Больше десятка на 1 308 слов.
3. **Точка после заголовка** в H1 (`Compliance that helps you close deals.`) и в H1 страницы `/pricing` (`Pricing tailored to your compliance scope.`).
4. **Дословный повтор подзаголовка** в двух разных секциях — след генерации по секциям без сквозной вычитки.
5. **Параллельная конструкция `Most platforms … We …`, повторённая 4 раза подряд** в секции 9. На третьем повторе приём становится слышен как приём.

**Не найдено (и это хорошо):** ни `unlock`, ни `seamless(ly)`, ни `effortless`, ни `empower`, ни `leverage`, ни `robust`, ни `cutting-edge`, ни `game-changing`, ни `elevate`, ни `revolutionize`, ни `transform` — проверено grep'ом по 11 маркерам, 0 совпадений в видимом тексте. Лексика на удивление чистая. Тик у этого текста **синтаксический, а не лексический** — и это ровно тот случай, который ловится линтером на пунктуацию и не ловится списком запрещённых слов.

---

## 5. Доказательства и доверие

### Логотипы клиентов
14 штук, бегущей лентой: `Dub, Persona, Corgi, Transloadit, Unkey, Inference, Better Auth, SST, Papermark, OpenCode, Primer, Modash, Dash Social, Assignar`. Отрисованы инлайн-SVG с `role="img"` и `aria-label` — **доступны скринридеру, в отличие от иконок интеграций**. Ни один логотип не кликабелен, кейса за ним нет.
*Статус: полу-проверяемо* — компании реальны и узнаваемы в dev-tool-среде, но связь «клиент» ничем на странице не подтверждена. Persona и Luthor AI пересекаются с отзывами, что усиливает именно их.

### Отзывы
**6 штук, все именные, все с должностью, все с компанией, все с фото.** Полные тексты — в разделе 1, секция 6.
*Статус: наиболее проверяемый актив страницы.* Аватары грузятся не из ассетов сайта, а через прокси Next.js с **Slack CDN** (`ca.slack-edge.com/T0702R613HQ-U0851S58RL3-…`) — то есть это профильные фото реальных людей из общих Slack-каналов. Пять из шести имеют полное имя и компанию, проверяемые снаружи; один (`Glenn E.`) сокращён, один (`Jana D., SessionLab`) без должности.
Ни один отзыв не содержит числа результата — только субъективную оценку, кроме первого (`30-40%`, `less than 2 weeks`).

### Числа и их источник
См. таблицу в разделе 4. Короткий вывод: **из девяти числовых заявок на главной ни одна не имеет ссылки на подтверждение.** `4.9/5` атрибутировано логотипом G2 (без ссылки и без количества отзывов). Остальные — голые.

### Кейсы
**На главной их нет вообще.** Ссылка `Customers` в шапке ведёт на `/case-studies`, где лежит настоящий арсенал, который на лендинг не вынесли (verbatim):
- `Why Persona AI switched from Vanta to Comp AI` — `$400,000+ ARR unlocked`, `6 days To audit-ready`, `85 hours Employee hours saved`
- `RiskInMind passed SOC 2 in 20 days and unlocked a $100K customer` — `20 days`, `120 hours`, `$100K ARR`
- `How a two-person startup passed SOC 2 and unlocked $50,000+ in stuck deals` (Patentia) — `$50,000+ Deals unlocked in 3 months`, `LatAm → U.S. Expanded into a new market`
- `How Zernio got audit-ready in days and won SOC 2 + GDPR in 3 months` — `Days`, `~200 hours`
- `How Anodes AI became HIPAA + SOC 2 audit-ready in 5 weeks to unlock pilots` — `8 days`, `103 hours`
- `How Luthor AI became SOC 2 Type II audit-ready in 2 weeks`

Каждый кейс — три метрики, и они ровно те, которые обещает H1 (деньги, время, часы). Ни одна цифра не появляется на главной.

### Скриншоты продукта
**Реальные, не иллюстрации.** Пять отдельных изображений фич (`/features/*.webp`) плюс четыре в таймлайне (`/how-it-works/*.webp`), все отданы через оптимизатор Next.js с `q=100` и `w=3840`. На скриншоте панели `Frameworks` видны настоящие данные состояния: `SOC 2 TYPE I — 92%`, `ISO 27001 — 35%`, `HIPAA — 50%`, `GDPR — 35%`. Прогресс намеренно **не 100%** — показан рабочий, а не идеальный экран.
*Статус: сильное доказательство.* Продукт показан, а не описан.

### Security / compliance-бейджи
Четыре печати в герое и четыре в футере: `SOC 2` (CERTIFIED), `ISO 27001` (CERTIFIED), `HIPAA` (COMPLIANT), `GDPR` (COMPLIANT). Отрисованы как инлайн-SVG, **не кликабельны**.
*Статус: полу-декоративно.* Но за ними стоит проверяемое: `View ours ↗` → `https://security.trycomp.ai` (собственный trust center) и `All Systems Normal` → `https://status.trycomp.ai`. То есть бейджи не кликабельны, но проверить их можно двумя другими путями с той же страницы. Продавец комплаенса, показывающий собственный trust center — это доказательство категорийного уровня: он предъявляет себя как своего же клиента.

### GitHub-звёзды
**Не показаны нигде на странице.** Ни счётчика, ни бейджа — только ссылки `View the full source on GitHub ↗` и `GitHub` в футере.
*Измеренная реальность:* `trycompai/comp` — **1 909 звёзд, 400 форков, 29 открытых issue, AGPL-3.0**, создан 2025-01-15, последний push 2026-08-09 (GitHub API). Это заметный актив, и он не используется.

### Соцпруф прочий
- `Trusted by 1,000+ companies from startups to enterprise` — под героем, дублируется на `/pricing`, `/case-studies`, `/vanta-pricing`
- `Trusted by teams who ship fast` — H2 секции отзывов
- Соцсети в футере: GitHub, X/Twitter, LinkedIn, YouTube
- В JSON-LD `sameAs` дополнительно указан `https://producthunt.com/posts/comp-ai` — **на самой странице ссылки на Product Hunt нет**

### Итог: что проверяемо, что декоративно

| Проверяемо (можно кликнуть и убедиться) | Декоративно (нужно поверить на слово) |
|---|---|
| Исходный код на GitHub — 3 ссылки на конкретные пакеты | `580+ integrations` (4 упоминания, ноль ссылок) |
| Собственный trust center `security.trycomp.ai` | `1,000+ companies` |
| Статус-страница `status.trycomp.ai` (`All Systems Normal`) | `4.9/5` (логотип G2 без ссылки и без числа отзывов) |
| 6 именных отзывов с фото из Slack CDN | 14 логотипов клиентов (не кликабельны) |
| Скриншоты продукта с реальными данными | 8 печатей SOC 2 / ISO / HIPAA / GDPR (не кликабельны) |
| Юрдокументы: DPA, SLA, Subprocessors | Сетка иконок интеграций (`aria-hidden="true"`) |
| Slack-тред с таймстемпами как доказательство «3 минут» | `99.9% uptime SLA` |

---

## 6. Механика конверсии

**Количество CTA и уникальных надписей.** 13 кликабельных CTA на главной, 3 уникальные надписи (`Get Started` ×7, `Book Demo` ×4, `Sign in` ×1) плюс `Book a Demo` ×1 в футере как четвёртая, лишняя.

**Первый CTA над сгибом?** Да. При 1562×784 форма `Enter your work email` + `Get Started` полностью видна в первом экране вместе с H1, подзаголовком, бейджем G2 и четырьмя печатями (проверено скриншотом). Ничего не требует прокрутки.

**Один путь или несколько.** Два, чётко разведённых по намерению:
- **Self-serve:** `Get Started` → инлайн-форма → `app.trycomp.ai`. Семь входов, все идентичные.
- **Sales-assisted:** `Book Demo` → `/demo` → 4-полевая форма → календарь. Пять входов (шапка, три таба, футер).

Третий, скрытый: **путь скептика** — четыре внешние ссылки на GitHub и trust center. Он не ведёт к конверсии напрямую и намеренно уводит с сайта. Для open-source-позиционирования это правильно: читатель, который проверил код, возвращается другим человеком.

**Форма и её поля.**
- **На главной: одно поле.** `<input type="email" name="work_email" placeholder="Enter your work email" inputMode="email" autoComplete="email" autoCapitalize="none" autoCorrect="off" spellCheck="false">`. Всего на странице **7 форм, 7 инпутов, одно уникальное имя поля** (`work_email`) — то есть все семь идентичны. Атрибуты выставлены аккуратно: на мобильном откроется email-клавиатура, автокоррекция выключена.
- **На `/demo`: четыре поля** — `First name`, `Last name`, `Work email`, `Company name`, кнопка `Next`.
- **На `/pricing`: четыре поля** — `First name`, `Last name`, `Work email`, `Company`, кнопка `Continue`, с явным индикатором `Step 1 of 3`.
- **Нет ни одного `<select>`** ни на одной из проверенных страниц: ни «размер компании», ни «нужный фреймворк» — квалификация полностью снята с формы и перенесена на звонок.

**Трение.** На главной — минимальное: одно поле, без обязательных чекбоксов, без капчи в разметке, без согласия на условия. Но у этого есть цена: **под формами главной нет ни строки о том, что произойдёт после отправки.** Ни `No credit card required`, ни `We'll email you a link`, ни ссылки на приватность. Читатель отдаёт рабочий email в никуда. На `/demo` и `/pricing` эта микрокопия есть (`No contract to sign`, `Money-back guarantee`, `By submitting, you agree to our Terms and Privacy Policy.`) — то есть страница с наименьшим доверием получила наименьшую поддержку.

**Как показаны цены.** Никак. Ноль ценовых сигналов на всей главной: ни числа, ни диапазона, ни «from $», ни «free tier», ни «free trial». Ссылка `Pricing` в шапке ведёт на страницу, где числа тоже нет — только форма и объяснение, почему числа нет (`Why don't you publish a price list?`). При этом JSON-LD той же главной объявляет `"offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free tools available"}` — то есть машине сообщается цена 0, человеку — ничего.

**Вторичные пути.**
- `Customers` → `/case-studies` (там лежат все сильные числа)
- `Pricing` → `/pricing` (форма вместо цены)
- `Sign in` → `app.trycomp.ai`
- Футер: `Compare` — 6 SEO-страниц против конкурентов; `Guides` — 6 страниц под problem-aware-трафик; `Compliance Hub`, `Tools & Templates`, `Documentation`
- 4 внешние ссылки-доказательства + статус-страница

**Sticky / exit-intent / чат.**
- **Sticky:** шапка фиксированная (`class="fixed inset-x-0 top-0 z-50"`, `data-marketing-header="true"`), с `backdrop-blur-xl`. Кнопка `Book Demo` в ней — единственный CTA, доступный на любой глубине прокрутки. Sticky-панели внизу нет.
- **Exit-intent:** не обнаружен ни в разметке, ни в сетевом логе.
- **Чат-виджет:** отсутствует. Это осознанно и согласуется с оффером — вместо чата на сайте продают `1:1 Slack support with real experts`, то есть поддержку внутри рабочего инструмента клиента, а не всплывашку.
- **Cookie-баннер:** есть, `c15t`, внизу слева, **не блокирующий** (страницу видно и можно скроллить). Три опции: `Reject` · `Accept` · `Choose` — причём `Reject` стоит первой и визуально равноправна `Accept`. Текст (verbatim): `Privacy choices — Optional cookies help us measure site performance and advertising.` Гео-осведомлён (`set-cookie: c15t-region=eu`). Для продавца комплаенса это часть продукта, а не юридическая формальность.

---

## 7. Визуал и движение

**Тип визуала.** Светлая страница со «врезанными» тёмными карточками. Герой — тёмно-зелёный градиентный прямоугольник со скруглениями и «выемками» углов (`corner-t-notch`, `corner-bevel`), сидящий внутри белой сетки с тонкими вертикальными направляющими по краям контента. Ощущение — не «страница с секциями», а «панель, разложенная на листе».

**Демо продукта.** Есть, и оно настоящее. Девять webp-скриншотов реального интерфейса (`/how-it-works/frameworks.webp`, `ai_agent.webp`, `slack.webp`, `trust_center.webp`; `/features/evidence_collection.webp`, `vendor_risk_monitoring.webp`, `device_agent.webp`, `penetration_tests.webp`, `cloud_monitoring.webp`). Плюс интерактивные моки: панель `Frameworks` с прогресс-барами, Slack-канал `#comp-ai-cx` с сообщениями и таймстемпами, граф интеграций с логотипами Auth0 и OpenAI. **Видео нет.**

**Анимации и скролл-эффекты (что удалось установить по разметке и наблюдению):**
- Вход элементов: в SSR у ключевых узлов стоит стартовое состояние `style="opacity:0;transform:translateY(12px)"` (H1), `translateY(10px)` (подзаголовок, форма), `translateY(16px)` (заголовки секций), `transform:scale(0.85)` (печати). То есть анимация появления описана как fade + подъём, оркестрованная лесенкой по величине смещения.
- Пословный/побуквенный reveal: наблюдался в шаге 2 таймлайна — текст `Auto-generate access control policies mapped to SOC 2 controls.` печатается с курсором.
- Бегущие ленты: логотипы клиентов и сетка интеграций (`<div class="flex w-max" style="gap:56px">` — классический marquee на трансформе).
- 3D: блок интеграций наклонён и распрямляется по ховеру — `class="rotate-x-6 hover:rotate-x-0 …"` в связке с `perspective-dramatic` на родителе.
- Маски затухания: `mask-radial-from-…`, `mask-radial-to-55%` — края лент растворяются, а не обрезаются.

**Деградация.** Двойственная и в одном месте опасная:
- *Хорошо:* весь смысловой контент присутствует в SSR-HTML. Без JS страница читается целиком (кроме FAQ-ответов и неактивных табов).
- *Плохо:* стартовые состояния анимации записаны **инлайн-стилями в SSR** (`opacity:0`). Если JS не выполнится или анимационный чанк не загрузится, H1 и подзаголовок останутся невидимыми. Это наблюдалось живьём: первый скриншот, снятый до завершения гидратации, показал герой **без формы и без печатей** — они были в DOM, но с `opacity:0`. Через несколько секунд появились. `prefers-reduced-motion` в проверенной разметке не встречается — **не проверено** отдельно, см. раздел 11.

**Ритм.** Чередование плотности вместо чередования цвета: тёмный герой → узкая полоса логотипов → просторный вертикальный таймлайн (5 шагов, самая длинная секция) → компактные табы → плотная сетка отзывов → сетка из 5 карточек → одна широкая визуальная секция интеграций → длинная текстовая секция из 6 аргументов → компактный FAQ → короткий финальный CTA → плотный футер. Ни одна секция не похожа по компоновке на соседнюю. CTA `Get Started` расставлены как метроном — после каждой смысловой единицы.

**Тема.** Светлая по умолчанию, с тёмными акцентными блоками. Палитра — зелёная моно: `#001A14 → #002C22 → #004D3A → #007A55` в градиенте героя, тёмно-зелёная заливка кнопок. Единственный чужой цвет на странице — красный `#FF492C` у звёзд G2, и он работает именно потому, что единственный. Токены названы семантически (`bg-background`, `text-foreground`, `bg-card`, `text-muted-foreground`, `border-foreground/5`) — то есть тёмная тема, вероятно, предусмотрена архитектурно; **фактическое наличие тёмной темы не проверено**.

**Типографика.** **TWK Lausanne** (Weltkern), self-hosted, **ровно два начертания: 400 и 700**. Один шрифт на всё, без пары. H1 — `text-4xl` на мобильном / `md:text-5xl` на десктопе, `leading-[1.1]`, `tracking-[-0.5px]` — плотный трекинг и почти сомкнутый интерлиньяж, типичная «продуктовая» настройка крупного кегля. Используется `text-balance` на заголовках и `text-pretty` на абзацах — то есть перенос строк отдан браузеру осознанно, а не разбит вручную.

---

## 8. SEO/AEO техника

**`<title>`** (verbatim, 41 символ):
`Comp AI: AI Compliance Software | Comp AI`
Бренд повторён дважды — в начале и в хвосте после разделителя. Похоже на шаблон `%s | Comp AI`, применённый к строке, которая уже содержала бренд. Мелкая, но реальная ошибка: 8 символов сниппета потрачены впустую.

**`<meta name="description">`** (verbatim, 134 символа):
`Automate SOC 2, ISO 27001, HIPAA, and GDPR. 580+ integrations, 1,000+ companies, audit-ready in days, with audit and pentest included.`
Плотная: четыре фреймворка + три числа + два включённых блага. Отмечу расхождение с самой страницей — `audit and pentest included` на главной **не заявлено ни разу**; этот аргумент живёт только на `/vanta-pricing` (`Audit + pen test bundled`). Description обещает то, чего на посадке нет.

**H1** (verbatim, 38 символов): `Compliance that helps you close deals.`
Ровно один H1 на странице (два вхождения в HTML — это shell + streaming-копия одного и того же узла, `<body>` в документе один).

**Иерархия заголовков.** Чистая, без пропусков уровней:
```
H1  Compliance that helps you close deals.
├─ H2  How it works
│   ├─ H3  Pick your frameworks
│   ├─ H3  Tailored to your business
│   ├─ H3  Continuous evidence collection
│   ├─ H3  1:1 Slack support with real experts
│   └─ H3  Share a live trust center
├─ H2  Compliance for every stage of growth
│   ├─ H3  Startup / H3 Mid-Market / H3 Enterprise
├─ H2  Trusted by teams who ship fast
├─ H2  The AI-first compliance platform
│   └─ H3  ×5 (фичи)
├─ H2  Connect with your existing stack
├─ H2  Compliance that actually improves your security
├─ H2  Frequently Asked Questions
│   ├─ H3  Platform / How It Works / Auditing  (категории)
│   └─ H3  ×7  (вопросы)
└─ H2  Don't let compliance slow down your pipeline
```
Замечание: секция 9 (шесть аргументов `01.`–`06.`) содержит **самый ценный текст страницы, и ни один из шести заголовков не размечен как H3** — они обычные `<div>`. Для машины эта секция — один сплошной абзац.

**schema.org.** Три блока `application/ld+json` (два уникальных, третий — дубль FAQ в стриминговой копии):
1. `@graph` из трёх сущностей:
   - `Organization` (`@id: …#organization`) — `name`, `url`, `logo`, `sameAs` на 5 площадок (GitHub, X, YouTube, LinkedIn, Product Hunt), `knowsAbout: ["SOC 2","ISO 27001","HIPAA","GDPR"]`, `potentialAction` → `https://app.trycomp.ai`
   - `WebSite` (`@id: …#website`) — с `publisher` по `@id`, `inLanguage: "en-US"`
   - `SoftwareApplication` (`@id: …#softwareapp`) — `applicationCategory: "BusinessApplication"`, `applicationSubCategory: "Compliance Software"`, `offers` с `"price": "0"`, и `aggregateRating: {"ratingValue": "4.7", "reviewCount": "64", "bestRating": "5"}`
2. `FAQPage` (`@id: …#faq`) — **все 7 вопросов с полными ответами**

Разметка сделана грамотно: сущности связаны через `@id`, а не продублированы. Два замечания: (а) `aggregateRating` 4.7 расходится с видимым `4.9/5`; (б) `offers.price = "0"` при полном отсутствии публичной цены — это заявка, которую страница не подтверждает.

**Open Graph / Twitter.** Полный комплект, без пропусков: `og:title`, `og:description`, `og:url`, `og:site_name`, `og:locale`, `og:type`, `og:image` (+ `:type`, `:width` 1200, `:height` 630, `:alt`); `twitter:card=summary_large_image`, `twitter:site=@compai`, `twitter:creator`, `twitter:title`, `twitter:description`, `twitter:image` (+ `:alt`, `:width`, `:height`). Изображение — `https://www.trycomp.ai/og.webp`.
Заголовок OG отличается от `<title>` и лучше него: `Comp AI: AI Compliance Software` — без дубля бренда.

**Canonical.** `<link rel="canonical" href="https://www.trycomp.ai"/>` — **без завершающего слэша**, при том что `og:url` тоже `https://www.trycomp.ai`, а `WebSite.url` в JSON-LD — `https://www.trycomp.ai/` **со слэшем**, и `sitemap.xml` тоже отдаёт `<loc>https://www.trycomp.ai/</loc>` со слэшем. Три источника, две формы. Мелочь, но именно такие мелочи размывают сигнал канонизации.

**hreflang.** Отсутствует. Сайт одноязычный (`og:locale: en`, `inLanguage: en-US`) — для текущего состояния корректно.

**robots.**
- Мета: `<meta name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>` — снят лимит на длину сниппета и разрешены крупные превью, то есть страница **явно приглашает выдачу цитировать себя длинно**.
- `/robots.txt` — и вот здесь самое интересное для AEO: там **отдельная секция для ботов OpenAI**:
```
User-Agent: OAI-AdsBot
User-Agent: OAI-SearchBot
Allow: /
Disallow: /api/
Disallow: /_proxy/
```
Общее правило при этом содержит `Disallow: /*?*` (все URL с query-строкой закрыты), а для `Googlebot`/`Bingbot` выставлен `Crawl-delay: 1`. Указаны `Host:` и **два** сайтмапа: `https://www.trycomp.ai/sitemap.xml` и `https://www.trycomp.ai/docs/sitemap.xml`.

**Sitemap.** Валидный XML с `lastmod` (`2026-08-21T22:59:02.648Z`), `changefreq` и `priority`. Главная — `priority 1`, `changefreq weekly`; `/demo` — `0.8`; сервисные страницы — `0.6`.

**Читается ли без JS.** **Да, почти полностью** — и это главное техническое достоинство страницы. В сыром HTML присутствуют H1, все H2/H3, все абзацы, все 6 отзывов с именами и должностями, все 6 аргументов секции 9, весь футер, все ссылки. **Два исключения:**
1. **Ответы FAQ отсутствуют в DOM.** Проверено строго: после удаления всех блоков `ld+json` из HTML строки `auditor-agnostic`, `Yes, 100%`, `around 10 days` не встречаются в разметке ни разу — все вхождения имеют `in_script=True`. Дополнительно подтверждено `get_page_text` в живом браузере после полной гидратации: вернулись только вопросы.
   **Следствие:** поисковик и LLM получают ответы через `FAQPage`-схему и, скорее всего, процитируют их. Человек без JS — и любой парсер, читающий видимый текст — не получит ничего. Ставка на то, что schema.org достаточна, довольно смелая.
2. **Неактивные табы не отрендерены.** Буллеты `Mid-Market` и `Enterprise` появляются только после гидратации (SSR — 3 буллета, после JS — 9).

**Внутренние ссылки.** ~45 уникальных внутренних адресов, и структура умная. Футер несёт два тематических кластера:
- `Guides` — под problem-aware-запросы: `/soc-2-cost`, `/soc-2-checklist`, `/soc-2-for-startups`, `/soc-1-vs-soc-2`, `/iso-42001`, `/grc-automation`
- `Compare` — под запросы сравнения и цены конкурентов: `/vanta-pricing`, `/drata-pricing`, `/secureframe-pricing`, `/drata-vs-vanta`, `/vanta-competitors`, `/drata-competitors`

Обратите внимание на `/drata-vs-vanta` — страница о сравнении **двух конкурентов между собой**, где Comp AI не участник. Классический захват середины: перехватить трафик человека, который ещё выбирает между двумя другими.

**Блог / FAQ.** Блога в навигации нет; вместо него `/hub` (`Compliance Hub`), `/tools` (`Tools & Templates`), `/docs` (`Documentation`, со своим сайтмапом). FAQ на главной — 7 вопросов, размеченных `FAQPage`, сгруппированных по трём темам (`Platform`, `How It Works`, `Auditing`). Вопросы сформулированы как реальные запросы (`How long does it take to get audit-ready?`, `Can I bring my own auditor?`), а ответы содержат прямые цифры (`audit-ready for SOC 2 Type I in around 10 days`) — то есть написаны с расчётом на извлечение, а не на чтение.

---

## 9. Слабые места

**1. Цена. Броня «нас можно проверить» пробита ровно там, где начинается счёт.**
Страница построена на утверждении `You don't take our word for it, you verify it.` и `Most compliance platforms are black boxes - you trust them because you have to.` При этом самое частое возражение — «сколько это стоит» — не имеет ответа нигде. `/pricing` отвечает на него формой и абзацем `Why don't you publish a price list?` → `Because a flat rate would overcharge simple programs and undercharge complex ones.` Аргумент разумный, но он в точности тот же, каким пользуется Vanta — которую они на `/vanta-pricing` критикуют словами `Pricing is not publicly listed and requires a sales call`. Публиковать оценку чужой цены (`$10,000 - $20,000/year`, `These ranges are based on market research`) и не публиковать свою — это единственное место, где страница уязвима для встречного удара.

**2. Все сильные числа спрятаны на клик глубже.**
На главной — ни одной денежной суммы и ни одного срока с числом. На `/case-studies` — `$400,000+ ARR unlocked`, `6 days To audit-ready`, `85 hours Employee hours saved`, `$100K ARR`, `$50,000+ Deals unlocked in 3 months`, `~200 hours`. Это буквальное доказательство обещания из H1 (`helps you close deals`), и оно не показано тому, кто читает H1.

**3. Ответы FAQ не существуют для человека без JS.**
Проверено: строки ответов присутствуют только внутри `<script type="application/ld+json">`; после гидратации в DOM их по-прежнему нет. Машина получает полный FAQ, человек — семь заголовков. Односторонняя оптимизация: страница, продающая прозрачность, прячет ответы от читателя и показывает их только краулеру.

**4. `4.9/5` на экране против `4.7 / 64 reviews` в разметке.**
Один и тот же документ сообщает человеку и машине разные оценки. Плюс `reviewCount: 64` — вполне достойное число — существует в JSON-LD и не показано на экране, хотя именно оно делает рейтинг достоверным. И бейдж не кликабелен: логотип G2 стоит, ссылки на профиль G2 нет.

**5. Под семью формами на главной нет ни строки микрокопии.**
Ни `No credit card required`, ни объяснения следующего шага, ни ссылки на приватность. При этом на `/demo` и `/pricing` микрокопия отличная (`20-min call · Quote emailed after · No contract to sign`, `Money-back guarantee`, `Step 1 of 3`). Поддержка выдана тем, кто уже согласился, и не выдана тем, кого ещё нужно убедить.

**6. Дословно повторённый подзаголовок в двух секциях.**
`Automate evidence collection, policy generation, and continuous monitoring - all from a single platform.` стоит и под `How it works`, и под `The AI-first compliance platform`. Один и тот же ответ на два разных вопроса — след генерации по секциям без сквозной вычитки.

**7. Одно действие — два имени, дважды.**
`Book Demo` (шапка, табы) против `Book a Demo` (футер). `Continue` (`/pricing`) против `Next` (`/demo`) для одинакового первого шага одинаковой формы. Мелочь, которая в реестре строк была бы поймана автоматически.

**8. Самая ценная секция не размечена заголовками.**
Шесть аргументов `01. Evidence that's never stale` … `06. Open source and verifiable` — лучший текст на странице — свёрстаны обычными `<div>`. Ни одного H3. Для машины это один длинный абзац без структуры.

**9. Description обещает то, чего на странице нет.**
`…with audit and pentest included.` — «включённый аудит» на главной не заявлен ни разу; `Penetration testing` упомянут как фича, но не как включённая в цену. Аргумент `Audit + pen test bundled … No surprise $10-30K costs at audit time` живёт только на `/vanta-pricing`. Это, вероятно, сильнейший коммерческий дифференциатор компании — и его нет на главной посадке.

**10. Анимация — единственная точка отказа для контента.**
Стартовое `opacity:0` записано инлайном в SSR. Наблюдалось живьём: первый скриншот показал герой без формы и без печатей. Если анимационный чанк не догрузится, первый экран останется наполовину пустым. Ирония в том, что страница отлично сделана для чтения без JS — и сама же ставит ключевые элементы в зависимость от JS.

**11. Иконки интеграций невидимы для скринридера.**
Контейнеры помечены `aria-hidden="true"`, названий нет. Логотипы клиентов при этом размечены правильно (`role="img" aria-label="…"`) — то есть команда знает, как надо, и в одном месте не сделала.

**12. Враг назван только чужим голосом.**
Единственное упоминание Vanta в теле страницы — внутри отзыва (`We were maybe 30-40% of the way through with Vanta when we switched`). Это осторожная тактика, но она стоит остроты: шесть блоков `Most platforms…` били бы вдвое сильнее хотя бы с одним именем.

**13. 1 909 звёзд GitHub не использованы.**
Позиционирование целиком построено на open-source, аудитория (Better Auth, SST, Unkey, OpenCode) считывает звёзды как валюту, актив измерен и реален — и на странице его нет.

**14. Дубль разметки удваивает вес документа.**
901 KB HTML, из которых ~440 KB — вторая копия той же разметки (React streaming: shell + `<div hidden id="S:0">`). Работает корректно, но это почти полмегабайта по проводу за архитектурное решение, которое здесь ничего не даёт: страница не имеет медленных данных, ради которых стоило бы стримить.

**15. Бренд двоится в `<title>`.**
`Comp AI: AI Compliance Software | Comp AI` — шаблон `| Comp AI` наложен на строку, уже содержащую бренд.

---

## 10. Переносимые приёмы

Отмечено: **[У]** — универсальный, **[К]** — специфичный для категории (compliance / enterprise-trust / продажа скептику).

### 1. [У] H1 обещает метрику читателя, а не свойство продукта
Формула: `<Категория> that <переопределённая роль> <метрика, за которую читатель отвечает>`.
Verbatim: `Compliance that helps you close deals.`
Контроль качества — на той же странице лежит антипример из их же H2: `The AI-first compliance platform`. Если ваш H1 можно поставить на сайт конкурента без правок, это второй тип.

### 2. [У] Подзаголовок берёт на себя всю фактуру, освобождая H1 для одного смысла
Verbatim: H1 `Compliance that helps you close deals.` (6 слов) → подзаголовок `SOC 2, ISO 27001, HIPAA, and GDPR - automated with 580+ integrations. We get you audit-ready.` (16 слов).
Разделение труда: H1 отвечает «зачем», подзаголовок — «что именно и сколько». Попытка вложить оба смысла в H1 убивает оба.

### 3. [У] Заявку доказывает артефакт, а не повтор числа
Verbatim: `Our in-house experts respond in under 3 minutes` — и рядом мок Slack-канала `#comp-ai-cx` с таймстемпами `Tom W. 2:34 PM` → `Comp AI Support 2:35 PM`.
Правило: рядом с каждым числом-обещанием ставьте артефакт, в котором это число видно как факт. Одна минута на скриншоте убеждает сильнее, чем «под 3 минуты» прописью.

### 4. [К] Отдавайте наружу ссылки, по которым вас можно проверить
Verbatim: `You don't take our word for it, you verify it.` + `View the full source on GitHub ↗`, `Integration platform on GitHub ↗`, `Device agent on GitHub ↗`, `View ours ↗`.
Ссылка на **конкретный пакет** (`/tree/main/packages/device-agent`), а не на корень репозитория — вот что делает приём работающим: читатель проверяет ровно то утверждение, которое только что прочёл. Категорийный приём: работает там, где покупают доверие (безопасность, комплаенс, инфраструктура, финансы).

### 5. [К] Продавец доверия предъявляет себя как своего же клиента
Verbatim: `View ours ↗` → `https://security.trycomp.ai`; `All Systems Normal` → `https://status.trycomp.ai`; в футере — `DPA`, `SLA`, `Subprocessors`.
Строка `Most trust centers are static marketing pages. Ours is live-monitored` работает только потому, что «ours» кликабельно. Аналог для любой категории: используйте собственный продукт публично и дайте на это ссылку.

### 6. [У] Формула контраста «Most platforms X → We Y», повторённая как структура секции
Verbatim: `Most platforms rely on manual screenshots and spreadsheets… We pull evidence continuously`; `Other platforms hand you generic policy documents and call it done… We generate every policy from the context you provide`; `Most trust centers are static marketing pages. Ours is live-monitored`.
Шесть блоков одной конструкции = шесть отработанных возражений без слова «возражение». **Предостережение из этого же примера:** на четвёртом повторе приём становится слышен. Три-четыре — потолок.

### 7. [У] Отрицание как способ описать выгоду
Verbatim: `no tickets, no email chains`; `No back and forth, no security review bottlenecks`; `in days, not weeks or months`; `reflects reality, not last quarter`; `not a template`; `no vendor lock-in, no black boxes`; `No two customers get the same boilerplate`.
Читателю проще опознать себя в том, чего он не хочет, чем в том, чего хочет. Считайте отрицания в своём тексте: у них семь на 1 308 слов.

### 8. [У] Конкретность через названный список, а не через слово-обобщение
Verbatim: `checking disk encryption, firewall status, screen lock, password length, and antivirus` вместо «мониторит устройства».
И через цитирование входа пользователя: `Say "show me that SSL is active on my domain"`. Пользовательская фраза в кавычках — самый дешёвый способ сделать фичу осязаемой.

### 9. [У] Конкретность через сцену
Verbatim: `A checklist doesn't stop a misconfigured laptop at 2am.`
Не число и не список — образ, который читатель может увидеть. Одна такая строка на секцию стоит абзаца характеристик.

### 10. [У] Одна надпись CTA на всю страницу, повторённая как метроном
13 CTA, 3 уникальные надписи. `Get Started` ×7 — по одному после каждой смысловой единицы, все ведут в одну форму с одним полем (`name="work_email"` — единственное имя поля на 7 форм).
Правило: столько CTA, сколько секций; столько надписей, сколько намерений. Их же нарушение возьмите как контрольный пример: `Book Demo` vs `Book a Demo`, `Continue` vs `Next`.

### 11. [У] Табы по стадии компании вместо тарифной сетки
Verbatim: `01 Startup` / `02 Mid-Market` / `03 Enterprise`, у каждого свой бенефит и свои три буллета (`SOC 2 Type I & II audit-ready in days, not weeks or months` … `Fully managed self-hosting` … `Dedicated compliance team with 99.9% uptime SLA`).
Даёт самоидентификацию и сегментированный аргумент без публикации цены. **Техническая оговорка из их же реализации:** рендерьте все табы в SSR — у них неактивные не попадают в HTML, и машина видит треть аргументов.

### 12. [К] Конкурента называет клиент, а не бренд
Verbatim: `We were maybe 30-40% of the way through with Vanta when we switched to Comp AI. In less than 2 weeks, we had everything in order to start our SOC 2 Type II observation period.` — Daniel Rascon, CTO, Persona AI.
Сравнение сделано, ответственность за него — на говорящем. В собственном голосе страницы конкурент не назван ни разу.

### 13. [У] Отзыв доказывается происхождением аватара
`src=/_next/image?url=https%3A%2F%2Fca.slack-edge.com%2FT0702R613HQ-U0851S58RL3-…` — все шесть фото тянутся с **Slack CDN**, а не из папки ассетов.
Имя + должность + компания + фото из рабочего инструмента = отзыв, который дороже подделать, чем написать. Плюс проверяемость: пять из шести имён гуглятся вместе с компанией.

### 14. [У] Скриншот с неидеальными данными убедительнее идеального
Панель `Frameworks` на первом шаге показывает `SOC 2 TYPE I — 92%`, `ISO 27001 — 35%`, `HIPAA — 50%`, `GDPR — 35%`. Ни одного 100%.
Рабочий экран читается как настоящий; вылизанный — как макет.

### 15. [К] Отдельная секция robots.txt под ботов ответных машин
```
User-Agent: OAI-AdsBot
User-Agent: OAI-SearchBot
Allow: /
Disallow: /api/
Disallow: /_proxy/
```
плюс `<meta name="robots" content="follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large">` — снятый лимит сниппета есть прямое приглашение цитировать длинно.
Переносится в любой публичный веб-продукт: решать про ботов ответных машин явно, а не по умолчанию.

### 16. [У] Схема как граф связанных `@id`, а не как набор дублей
`Organization` (`#organization`), `WebSite` (`#website`, ссылается на publisher по `@id`), `SoftwareApplication` (`#softwareapp`), `FAQPage` (`#faq`) — все в одном `@graph`, связанные ссылками, а не копиями полей.
**И их же ошибка как контрольный пример:** `aggregateRating: 4.7 / 64` в схеме против `4.9/5` на экране, `offers.price: "0"` при полном отсутствии публичной цены. Схема — это заявление; расхождение с видимым текстом обнаруживается тривиально.

### 17. [У] Footer как два SEO-плацдарма, а не как список ссылок
Кластер `Guides` (`/soc-2-cost`, `/soc-2-checklist`, `/soc-2-for-startups`, `/soc-1-vs-soc-2`, `/iso-42001`, `/grc-automation`) ловит problem-aware-трафик, которому главная не адресована. Кластер `Compare` (`/vanta-pricing`, `/drata-pricing`, `/secureframe-pricing`, `/drata-vs-vanta`, `/vanta-competitors`, `/drata-competitors`) ловит сравнивающих.
Отдельно отмечу `/drata-vs-vanta` — **страница о сравнении двух конкурентов между собой**, где бренд не участник. Перехват середины воронки.

### 18. [У] Проверяйте текст на синтаксический тик, а не только на словарь
Измерено на этой странице: `unlock`, `seamless`, `effortless`, `empower`, `leverage`, `robust`, `cutting-edge`, `elevate`, `transform` — **0 совпадений**. Словарь чистый.
При этом: **20 риторических тире** (все как ` - `, ноль em-dash), больше десятка триад `X, Y, and Z`, точка после H1, дословно повторённый подзаголовок.
Вывод для нашего линтера: замена `—` на ` - ` **не убирает тик** — она меняет глиф и сохраняет синтаксическую роль. Правило должно ловить тире-заместитель по функции (стоит вместо запятой/двоеточия/точки), а не по символу. И косвенная улика метода: на `/demo` уцелели 3 em-dash, на `/pricing` — ноль тире и 2 типографских апострофа. Три страницы прошли через разную обработку, и это видно по пунктуации.

### 19. [У] Микрокопия обязана стоять под самой ранней формой, а не под самой поздней
Контрпример отсюда: под семью формами главной — ноль строк поддержки; на `/demo` — `20-min call · Quote emailed after · No contract to sign`; на `/pricing` — `20 minutes · Pick your own time · Money-back guarantee` и `Step 1 of 3`.
Поддержка нужнее всего там, где доверие минимально. Если микрокопия есть только в глубине воронки — она стоит не в том месте.

### 20. [К] Продавайте цену конкурента, только если готовы показать свою
Verbatim с `/vanta-pricing`: `Startup — $10,000 - $20,000/year`, `Hidden costs`, `Additional frameworks: $5,000 - $15,000 each`, при оговорке `These ranges are based on market research`.
Verbatim с собственного `/pricing`: `Why don't you publish a price list?`
Приём мощный и работающий, но он **создаёт долг**. Обвинение в непрозрачности читается иначе, когда у обвинителя цены тоже нет. Переносить — вместе с обязательством показать хотя бы вилку или «from».

### 21. [У] Весь смысл — в SSR; на JS оставляйте только украшения
1 308 слов, все заголовки, все отзывы, весь футер читаются без единой строки исполненного JS.
**И их же нарушение как предостережение:** стартовое `opacity:0` записано инлайном в SSR, поэтому герой без JS остаётся наполовину невидимым (наблюдалось: первый скриншот — без формы и печатей). Правило: начальное состояние анимации ставится из JS после проверки его наличия, а не пишется в SSR-разметку.

### 22. [У] Ритм секций строится чередованием плотности, а не цвета
Тёмный герой → узкая лента логотипов → просторный таймлайн на 5 шагов → компактные табы → плотная сетка отзывов → 5 карточек → одна широкая визуальная секция → длинная текстовая на 6 блоков → компактный FAQ → короткий CTA → плотный футер.
Ни одна секция не повторяет компоновку соседней. Проверка для своей страницы: если две соседние секции — это «заголовок + три карточки», одна из них лишняя.

### 23. [У] Один шрифт, два начертания, один акцентный цвет
TWK Lausanne 400/700, зелёная монохромная палитра (`#001A14 → #007A55`), и ровно один чужой цвет на странице — `#FF492C` у звёзд G2.
Единственный контрастный цвет работает именно потому, что единственный. Как только их два, оба перестают быть акцентом.

### 24. [У] Кольцевая композиция: финальный CTA возвращает H1 в другой модальности
Открытие: `Compliance that helps you close deals.` (позитив: поможет).
Закрытие: `Don't let compliance slow down your pipeline` (негатив: не дай затормозить).
Одна мысль, два рычага — надежда в начале, потеря в конце. Дешёвый и надёжный способ сделать длинную страницу цельной.

---

## 11. Что не удалось проверить

1. **Что грузится после согласия на куки.** Все измерения сети сделаны до нажатия `Accept`. 38 запросов, все first-party. Какие пиксели, аналитика или session recording активируются c15t после согласия — **не проверено** (нажимать `Accept` не стал: это принятие условий от лица пользователя).
2. **Что происходит после отправки формы.** Ни одна из 7 форм не отправлялась. Куда уходит `work_email`, какой экран показывается, приходит ли письмо — **не проверено**.
3. **Содержимое дропдаунов `Product` и `Frameworks`** в шапке. Они рендерятся по клику и в SSR отсутствуют. **Не проверено** — кликать по ним не стал, чтобы не открывать состояния с формами.
4. **Наличие тёмной темы.** Токены названы семантически (`bg-background`, `text-foreground`), что обычно означает подготовленную тёмную тему, но переключателя на странице нет и `prefers-color-scheme` в проверенной разметке не встретился. **Не проверено.**
5. **`prefers-reduced-motion`.** В извлечённых инлайн-стилях и в именах классов правило не встретилось, но CSS вынесен в два внешних чанка (`246jt6w8b3f2m.css`, `3xopqco4xu_4b.css`), которые я не разбирал. **Не проверено.**
6. **Мобильная версия.** Все наблюдения сделаны на 1562×784. Классы `md:` в разметке присутствуют (`md:text-5xl`), то есть адаптив есть, но фактическое мобильное поведение — порядок секций, поведение sticky-шапки, ширина формы — **не проверено**.
7. **Core Web Vitals, LCP, вес после гидратации.** Измерен только вес HTML-документа (901 235 байт) и состав первой загрузки (38 запросов). Реальные метрики производительности **не измерялись**.
8. **Точное число интеграций.** `580+` повторено 4 раза; каталога, который можно пересчитать, на сайте не найдено. **Не проверено.**
9. **Число клиентов.** `1,000+ companies` — **не проверено**, источника нет ни на странице, ни в схеме.
10. **Рейтинг G2.** Бейдж `4.9/5` не кликабелен, ссылки на профиль G2 нет. Расхождение с `aggregateRating 4.7 / 64` в JSON-LD зафиксировано, но **какое из чисел актуально — не проверено** (профиль G2 не открывался).
11. **Цена Comp AI.** WebSearch вернул сторонние публикации со ссылкой на тарифы `$199/month (Starter)`, `$997/month (Pro)` и `$3,000 one-time`, а также AGPL-3.0 self-hosting без лицензионных отчислений. **На самом сайте ни одно из этих чисел не подтверждается — ни на главной, ни на `/pricing`.** Приводится как контекст третьих лиц, не как факт о странице.
12. **Финансирование.** WebSearch: `$2.6M`, инвесторы Grand Ventures, OSS Capital, Vercel; основатели Lewis Carhart, Claudio Fuentes, Mariano Fuentes; выход из stealth в апреле 2025. **Третьи лица, на сайте не заявлено** (раздел `/press` не открывался).
13. **Точность оценок цен конкурентов** на `/vanta-pricing` (`$10,000 - $20,000/year` и т. д.). Сама страница помечает их как `These ranges are based on market research`. **Независимо не проверено.**
14. **Полный список логотипов интеграций.** В сетке ~37 инлайн-SVG; по id-атрибутам опознаны только `vscode`, `vscodium`, `gemini`, визуально — Auth0 и OpenAI в графе шага 3. Контейнеры помечены `aria-hidden="true"`, названий в дереве доступности нет. **Полный список не установлен.**
15. **Подстраницы за пределами пяти снятых.** Проверены `/`, `/pricing`, `/demo`, `/case-studies`, `/vanta-pricing`, плюс `robots.txt` и `sitemap.xml`. Не открывались: `/security`(скачан, не разобран), `/hub`, `/tools`, `/docs`, `/press`, `/careers`, `/partnerships`, `security.trycomp.ai`, `status.trycomp.ai`, остальные страницы кластеров `Guides` и `Compare`.
16. **Существует ли A/B-тест на этой странице.** Ни фреймворка сплит-тестирования, ни флагов в разметке не найдено, но отсутствие следов в одном снимке не есть доказательство отсутствия. **Не проверено.**

---

*Снято 2026-08-30. Первичный источник — сырой HTML (`curl`, 901 235 байт) и живой рендер в Chrome. Вторичные — WebFetch (сверка текста), GitHub API (репозиторий), WebSearch (контекст рынка, помечен как непроверенный).*
