# Предложение: усиление режима дизайн-ревью (Mode D)

> Статус: **предложение к обсуждению**, не внедрено. Нарратив — на русском; конкретные артефакты (шаблоны, поля, пример ревью) — на английском, потому что они уйдут в англоязычные файлы скилла как есть.
>
> Как получено: 6 агентов с ролями. Фаза 1 — три аналитика (практик-критик, аудитор системы оценки, креативный директор) нашли сильные/слабые стороны Mode D с цитатами `file:line`. Фаза 2 — три исследователя (методолог UX-критики, бренд-стратег, куратор источников) нашли проверяемые внешние методики. Фаза 3 — этот синтез.

---

## TL;DR — что предлагается

Ревью сейчас «плавает» не из-за тона, а из-за **структуры**: шаблон называет проблемы в одних секциях, а фиксы — в другой, между ними нет связи; во всём репозитории **ноль** формулировок предсказанного эффекта; балл показывается только текущий; смелые ходы запрещены by design. Пять предложений, каждое закрывает конкретный разрыв:

1. **Единый блок Finding** — каждая находка становится одной причинной цепочкой: *что вижу → какой принцип нарушен → чем вредит пользователю → что изменить → к чему это приведёт → severity → какой балл двигает*. Закрывает требование «измени это, потому что X, что приведёт к Y».
2. **Оценка before/after** — текущий балл + спрогнозированный балл после правок, по измерениям, честно-условный («4/5, ЕСЛИ зайдут фиксы F1, F3 и подтвердятся допущения»). Закрывает требование «оценка сейчас и после правок».
3. **Блок Bold move** — отдельный, карантинный канал для смелого хода, который *противоречит продукту*, но усиливает UX, с явным trade-off и планом проверки. Закрывает требование «предложить и указать, что тут уходим в сторону, но усиливаем вот это».
4. **Операционализация креатива** — «красивее/лучше/отличительнее» переведены в проверяемые рычаги (счётчик/токен/да-нет), а не вкусовые слова. Плюс тест «безликого экрана», из-за которого технически-корректный-но-забываемый экран теряет балл.
5. **Inspiration v2 + генеративный метод** — источники вне Apple/Google (3 уровня) и пошаговый метод *выведения* свежего направления вместо листания галерей.

Главное: всё это встраивается **внутрь** существующей дисциплины доказательств (D1–D4, запрет «эстетической отмывки», severity по влиянию на пользователя), а не вместо неё. Смелость и креатив получают *более высокую* планку доказательности, а не послабление.

---

## 1. Оценка текущего состояния Mode D

Применяю принцип, который сам и предлагаю (before/after), к самому скиллу. Оцениваю Mode D **как инструмент ревью**, по рубрике скилла (`docs/design-quality-rubric.md`).

**Текущий балл: 3/5 — «acceptable baseline, competent rather than strong».**

Что держит на 3, а не выше (это и есть жалоба «плавает»):

| Измерение инструмента ревью | Сейчас | Почему |
|---|---|---|
| Дисциплина доказательств (D1–D4, границы) | 5/5 | Лучшая черта. Классификация суб-кейсов, запрет визуальных утверждений на тексте, обязательная «сильная сторона». Ломать нельзя. |
| Конкретность находок | 2/5 | Проблемы и фиксы живут в разных секциях, не связаны (`skill/templates.md:270-294` vs `:296-299`). |
| Причинность (зачем → к чему) | 1/5 | **Ноль** формулировок предсказанного эффекта во всём репо. Фикс — это глагол-команда без последствия. |
| Прогноз ценности (before/after) | 1/5 | Показывается только текущий балл (`examples/review-screen.md:63`). «Лестница улучшений» (`docs/design-quality-rubric.md:115-124`) существует, но не подключена к выходу. |
| Креативный диапазон / смелость | 1/5 | Нет канала под смелый ход; новизна прямо запрещена (`skill/skill.md:215`); «креативно» определено только негативно. |

Медиана тянется вниз двумя критичными измерениями (конкретность и причинность) — ровно теми, на которые жалуется владелец. Это здоровый диагноз: фундамент крепкий, надстройка отсутствует.

**Целевой балл после внедрения: 4/5** (условно — при внедрении Предложений 1–3 и регенерации эталонного примера). 5/5 потребует ещё и обновлённого eval-набора + golden-примеров + полевой проверки, что ревью реально стали точнее (см. §10).

---

## 2. Корневые причины «плавающего» ревью

Свёрнуто из Фазы 1 (все три аналитика сошлись независимо):

- **R1. Разрыв «проблема ↔ фикс».** Шаблон D перечисляет 6 корзин проблем и отдельно — плоский список фиксов. Нет поля, связывающего конкретный фикс с конкретной проблемой. Читатель сам домысливает связь. (`skill/templates.md:270-299`)
- **R2. Нет языка последствия.** Поиск по репо (`predicted effect`, `leads to`, `so that`, `will lead to`) — 0 совпадений в `skill/`, `docs/`, `examples/`. Единственное место, где есть хотя бы «...so users can compare amounts down a column» — это иллюстрация в анти-паттернах (`examples/anti-patterns.md:208`), и даже она не доходит до эффекта на балл.
- **R3. Балл статичен.** `Current design quality score: [1-5]/5` — один слот, настоящее время (`skill/templates.md:283`). Движок прогноза (8 измерений + лестница + условные кэпы) лежит рядом, но не подключён к Mode D.
- **R4. Смелость подавлена.** У Mode D нет поля `Key decision tradeoffs` (оно есть у Mode C и F — `skill/templates.md:242-244`, `:401-403`), а гайдрейлы трактуют «противоречит задаче» как провал (`examples/anti-patterns.md:197`). Добросовестный ревьюер по этому скиллу *избегает* смелого хода.
- **R5. Self-review не ловит цепочку.** Гейт Mode D (`docs/self-review.md:121-126`) проверяет всё, кроме связки «проблема→фикс→эффект» и наличия прогноза. Поэтому плавающее ревью проходит контроль чисто.

---

## 3. Предложение 1 — Единый блок Finding (требование №1)

**Суть.** Удалить раздельные секции `Usability issues / … / Recommended fixes` и заменить их одной повторяемой единицей **Finding**, где причинная цепочка собрана в одном месте. Лейблы линз (usability/a11y/...) сохраняются как тег `Lens:`, чтобы ничего не потерять.

**Почему это работает (источники).**
- Структура «объект → нарушенный принцип → последствие → рекомендация» — это формат отчёта *эвристической оценки* Нильсена и логика *критики* из Connor & Irizarry, *Discussing Design* (критика = разбор соответствия цели, а не реакция «не нравится»). NN/g «Making Usability Findings Actionable» (Schade, 2013) даёт 5 правил: называй конкретный элемент; формулируй как дефект дизайна, а не вину пользователя; отделяй структурное от косметического; помечай рекомендации как стартовые точки; ранжируй и балансируй сильными сторонами.
- Severity — **шкала Нильсена 0–4** (1994), считаемая как `frequency × impact × persistence`. Это убирает «severity на глаз».
- «Предсказанный эффект» формулируется грамматикой гипотез из CRO (Craig Sullivan «Hypothesis Kit»): *направленно + с уровнем уверенности + условно*, **никаких выдуманных процентов**.
- Для форм (а флагманский пример ревью — это форма!) добавить именованный источник: Luke Wroblewski, *Web Form Design* (2008). Для «перегруза» — теория когнитивной нагрузки (Sweller, 1988, «extraneous load»).

**Литеральный шаблон (в `skill/templates.md`, заменяет строки 270–299):**

```md
## Findings
> Each finding is one causal chain, ordered by severity. High-severity (3–4)
> findings use all fields. Low/cosmetic (0–2) may compress to
> Observation → Change → Severity. Never split an issue from its fix.

### F1 — [short title]
- Lens: [Usability / Accessibility / Hierarchy & readability / Design quality / Navigation]
- Observation: [what is there now — evidence-bound; for D2, structure & behavior only, no visual assertions]
- Violated principle: [named — e.g. Nielsen #5 Error prevention · Hick's Law · Cognitive load (extraneous) · Gestalt proximity · Wroblewski form-design]
- User consequence: [the mechanism by which it hurts the user — not a restatement of the observation]
- Change: [the specific edit]
- Predicted effect: [directional + confidence — "should reduce mis-submits; confidence M (D2 text-only)". NEVER a fabricated %]
- Severity: [0–4, Nielsen] — [frequency × impact × persistence, one line]
- Moves: [dimension band→band, e.g. "Hierarchy 2→4"; + "lifts cap: missing-states" if applicable]

### F2 — …
```

**Сопутствующее:**
- В `docs/self-review.md` (после строки 126) добавить три проверки Mode D: «каждый Finding связывает observation → why → change → predicted effect в одном месте?»; «нет ли фикса-сироты без родительской проблемы?»; «каждый predicted effect называет пользовательский исход, а не повторяет изменение?».
- В `docs/evals.md` (рядом с `:184`) — content-check: «нетривиальный фикс называет нарушенный принцип и предсказанный эффект».
- В `docs/heuristics.md` и `docs/sources.md` добавить: Cognitive Load Theory (Sweller), *Web Form Design* (Wroblewski), *Laws of UX* (Yablonski, 2020) как зонтичную ссылку на Fitts/Hick/Doherty/Jakob.

---

## 4. Предложение 2 — Оценка before/after (требование №2)

**Суть.** Показывать не только текущий балл, но и **спрогнозированный** — по измерениям, выведенный из уже существующей «лестницы улучшений», и **честно-условный**.

**Почему это работает (источники).**
- Прецедент оценки «до/после» в UX устойчив: дельты SUS (Sauro & Lewis, *Quantifying the User Experience*, 2016), повторная эвристическая оценка после правок (Нильсен).
- Движок уже есть в скилле: 8 измерений (`docs/design-quality-rubric.md:76-86`), «лестница» 1→2→3→4 (`:115-124`), условные кэпы с формулировками «until fixed / until translated» (`:91-99`). Прогноз — это та же лестница, наведённая на *рецензируемый* артефакт, а не на собственный черновик.

**Правила честности (критично — иначе променяем «плавающее» ревью на «самоуверенное»):**
1. **Условная грамматика обязательна.** Любой after-балл пишется как «projected N/5 **IF** [фиксы] зайдут **AND** [допущения] подтверждены». Голого after-числа не бывает.
2. **Кэп снимается только при выполнении его условия** и только если он снимаем. P0 / ложные заявления о compliance = **Fail**, не снимается фиксами и числом не прогнозируется.
3. **D2/D3 — дважды условно.** Текстовое ревью уже делает балл «provisional»; прогноз наследует это и добавляет: визуальные измерения (контраст, точный spacing) не прогнозируются вверх, уходят в `Unresolved assumptions`.
4. **Потолок прогноза по умолчанию — 4/5.** 5/5 только если перечислены и подтверждаемы условия устойчивости.
5. **Дельта считается по медиане, не суммой.** Починка одного измерения может не двинуть общий балл (если оно не медианное), и серьёзный неустранённый изъян по-прежнему тянет вниз. Это и есть защита от инфляции «починил три штуки → +3 балла».

**Литеральный шаблон (заменяет строку 283 в `skill/templates.md`):**

> Note (post-senior-review v1.16.1): the projected line is a **flat median of the assessable dimensions**, not "up to N/5"; any higher post-visual-pass figure lives only in `Ceiling note`. Visual dimensions stay `n/v` in D2/D3 and are never projected upward.

```md
## Design quality score (current → projected)
- Current: [n]/5 — [evidence-based reason; "provisional" for D2/D3]
- Projected: [m]/5 — median of the assessable projected dimensions once the listed fixes land; conditional: requires F[..] AND [assumptions]. Flat number, not "up to". [D2/D3: provisional — visual dimensions stay n/v.]
- Ceiling note: with a visual pass confirming [x], the ceiling is [1-5]/5 (capped at 4/5 unless resilience is named).
- Primary lever(s): [the one or two findings that move the score most]

| Dimension | Now | Projected | Gated by (cap / ladder rung) | Confidence |
|-----------|-----|-----------|------------------------------|------------|
| Attention path & hierarchy | [n] | [n] | [cap line / rung / —] | [verifiable / provisional / not-from-text] |
| Composition & spacing | [n] | [n] | … | … |
| Typography craft | [n] | [n] | … | … |
| Color, state & contrast | [n] | [n] | … | … |
| Density & rhythm | [n] | [n] | … | … |
| Interaction polish & motion | [n] | [n] | … | … |
| Context & brand fit | [n] | [n] | … | … |
| Production readiness | [n] | [n] | … | … |
- Projected overall = median of the assessable (non-n/v) projected dimensions, lowered if a critical task dimension stays weak. NOT the sum of per-dimension gains.
```

**Сопутствующее:** обновить правило вывода ревью в `docs/design-quality-rubric.md:44-48` (требовать оба числа), и eval в `docs/evals.md:267-269` (проверять условную грамматику, потолок 4/5, provisional для D2/D3, отсутствие числа при Fail).

---

## 5. Предложение 3 — Блок Bold move (требование №3)

**Суть.** Один санкционированный, **карантинный** канал для рекомендации, которая *противоречит текущему продукту/направлению*, но усиливает UX — с явным trade-off и планом проверки. Карантин — это весь трюк: смелый ход держится на *более высокой* планке доказательности, чем обычный фикс, и стоит **после** обязательных фиксов, чтобы не подменять их.

**Почему это работает (источники).**
- Право противоречить продукту даёт **Jobs-to-be-Done** (Christensen/Ulwick/Moesta): если фича служит продукту, но не «работе» пользователя — JTBD легитимизирует её слом. Ulwick даёт измеримую грамматику исхода: `minimize/increase [метрика] of [объект] when [контекст]`.
- Рамка «провокация, а не директива» — speculative/critical design (Dunne & Raby, *Speculative Everything*, 2013): смелый артефакт как ставка к проверке, а не приказ. Это и отделяет «смело» от «безрассудно».
- Контрарный дефолт «убрать, а не добавить» — Dieter Rams, принцип №10 («as little design as possible»).
- Что нельзя ломать: рекомендация, противоречащая задаче, остаётся провалом, **если её оправдание эстетическое**. Противоречие, обоснованное названным механизмом usability/a11y/иерархии и вынесенное в блок Bold move с trade-off, — поощряется.

**Триггер (когда вообще предлагать):** только если выполнено всё — нет неустранённой находки severity 3–4; экран уже ≥3/5, но *инертен* (баллов не теряет, но и лица не имеет); есть конкретный UX-апсайд. Разрешено в D1/D3; в D2 — только структура/поток, не визуал; в D4 — только если новый контекст это и открывает. Не уверен — **опусти секцию**. Максимум один ход (два — если реально разные).

**Литеральный шаблон (в `skill/templates.md`, после `Recommended fixes` / `Findings`, до `Platform-convention mismatches`):**

```md
## Bold move (optional — omit unless the trigger is met)
> Use only when: no unresolved severity-3/4 finding, the screen is already ≥3/5 but
> inert, and there is a concrete UX upside. Allowed in D1/D3; D2 = structure/flow
> only; D4 = only if the new context unlocks it. This is NOT a fix and NOT required
> to ship. At most one (two only if genuinely distinct). If unsure, omit.

- The move: [one buildable sentence — a component/layout/flow/interaction change, not an adjective]
- Deviates from: [the product assumption / current direction / brand rule / platform convention it contradicts]
- Job served (JTBD): [the job + one desired-outcome statement: minimize/increase [metric] of [object] when [context]]
- UX upside: [concrete, checkable benefit — tie to a named heuristic or quality bar]
- Risk / cost: [learnability, discoverability, accessibility exposure, or dev cost if this is wrong]
- De-risk / validate: [the cheap test before committing + kill criterion + the contrast/large-text/reduced-motion checks it must still pass]
- Score impact: safe fixes alone → [X]/5; this move targets [Y]/5; it does NOT raise the score until validated.
- Conviction: [Speculative / Worth a spike / High-confidence]
```

**Сопутствующее (firewall против «эстетической отмывки»):**
- Карваут в `docs/guardrails.md` и заметка к анти-паттерну 4 (`examples/anti-patterns.md:197`): «противоречие задаче = провал ТОЛЬКО при эстетическом оправдании; обоснованное названным UX-механизмом и вынесенное в Bold move — поощряется».
- Self-review (`docs/self-review.md`): «придержал ли я UX-усиливающую рекомендацию только потому, что она противоречит текущему продукту? Если да — перенеси в Bold move с trade-off».
- Bold move **не может** появляться в `Severity` или `Recommended fixes` и **не может** служить поводом пропустить фикс.
- Пара Bad/Good в `examples/anti-patterns.md` (Bad: «сделать дашборд премиальнее жирным героем» — нет механизма; Good: «заменить 5-табовую нижнюю навигацию на 3 таба + контекстный action bar; ломает принцип "всё в один тап"; служит работе X; апсайд — снижение выбора (Хик) и освобождение зоны большого пальца (Фиттс); риск — два раздела на уровень глубже; проверка — tree-test находимости + коуч-марк; балл: safe→4/5, цель 5/5 при подтверждении; conviction: worth a spike»).

---

## 6. Предложение 4 — Операционализация креатива

**Суть.** Перевести «креативно / лучше / отличительнее / премиально» в **проверяемые рычаги** (счёт, токен, да/нет), которые переживают анти-эстетическую дисциплину. Эти рычаги — кросс-режимные: живут в `docs/design-quality.md` и рубрике, а Mode D потребляет их через балл и Bold move.

**Ключевой контр-вес: тест «безликого экрана».** Один вопрос в `docs/self-review.md` и рубрике: *«Если убрать логотип и фирменный цвет — отличим ли экран от конкурента? Если нет — он инертен.»* Экран, компетентный по всем 8 измерениям, но проваливший этот тест, помечается **3/5 с пометкой об апсайде**, а не тихо ставится 4/5. Это и есть та «пружина» к отличительности, которой сейчас нет (сейчас безликий-но-аккуратный экран спокойно берёт 4/5).

**Набор рычагов (каждый = название · проверка · источник · гайдрейл от отмывки):**

| # | Рычаг | Проверка (счёт/токен/да-нет) | Источник | Гайдрейл |
|---|---|---|---|---|
| 1 | **Onlyness-тест** | Можно ли закончить «Это единственный [категория], который [конкретный ход]…» *без* вкусового слова? да/нет | Neumeier, *Zag* (2007) | Если заполняется только «премиально/современно» — провал: это полировка, не отличие. |
| 2 | **Аудит отличительных активов** | Сосчитать собственные, не-зависящие-от-имени активы экрана; классифицировать по уникальности. Забываемый = 0; отличительный = ≥1 в высокоуникальной колонке. | Sharp & Romaniuk, *Building Distinctive Brand Assets* (2018) | Актив должен быть *повторяемым*, иначе fame=0 → поощряет смелое применение существующего актива, отвергает одноразовый декор. Совместимо с анти-новизной. |
| 3 | **Гейт размещения делайта (Kano)** | Делайт оправдан только если элемент классифицируется как **Attractive**, не Must-be/Performance. да/нет | Kano et al. (1984) | Блокирует «сделать делайтовее» поверх отсутствующей обязательной функции. |
| 4 | **Тег уровня Нормана + проверка цены** | Пометить ход visceral/behavioral/reflective; подтвердить, что он не повышает behavioral-цену (лишний тап, задержка фидбэка). да/нет | Norman, *Emotional Design* (2004) | Висцеральный росчерк, купленный поведенческим долгом, — провал. |
| 5 | **Бюджет бренд-выражения** | ≤1 сигнатурный *перцептивный* ход на экран (≤2 на поток); функциональные паттерны — вне бюджета. счёт | Kholmatova, *Design Systems* (2017) | Выражение, потраченное на функциональный паттерн (где кнопка, что делает жест), = нарушение Jakob, авто-отказ. |
| 6 | **Токены motion-личности** | Задать диапазон длительности (200–500 мс), именованную easing-кривую под бренд-прилагательное, ровно один сигнатурный переход. токены, не прилагательные | Val Head, *Designing Interface Animation* (2016) | >500 мс или задержка фидбэка — провал по числам Head; расширяет диапазон, сохраняя запрет «700 мс премиум-перехода». |
| 7 | **Сплит type-личности** | Характерный шрифт — только в display-ролях; body/UI-текст на читаемом шрифте. да/нет по роли | Lupton, *Thinking with Type* (2010) | Характер, текущий в основной текст, — провал; отличительный голос без вреда читаемости. |

**Где это в Mode D:** рычаги 1–2 и тест инертности могут породить *находку* («экран инертен — нулевой отличительный актив, см. Bold move») или питают строку `Context & brand fit` в таблице баллов; рычаги 3–7 чаще работают в режимах генерации (A/C/E), но Mode D ссылается на них, оценивая design quality.

---

## 7. Предложение 5 — Inspiration v2 + генеративный метод

**Суть.** Сейчас `docs/inspiration-sources.md` — это плоский список галерей (Mobbin, Dribbble, Behance…), выключенный по умолчанию, без метода *выведения* направления. Заменяем на 3 уровня + пошаговый генеративный метод. Всё — вне Apple/Google, но с сохранением правила «инспирация ≠ доказательство usability/a11y/платформы/compliance», и с разделением production- и portfolio-источников.

**Уровень A — источники-рассуждения (учат «почему», чего галерея не может):** Airbnb Design (DLS «Building a Visual Language»), The Linear Method (`linear.app/method`), Stripe design/engineering writing, Figma blog, Intercom product principles, Spotify Design (Encore), Shopify Polaris (с обоснованиями), Smashing Magazine, A List Apart. Уже-доказательные (GOV.UK, NHS, NN/g, Monzo writing system) остаются в `sources.md`, не понижаются до «инспо».

**Уровень B — редакторские/типографические/композиционные школы (расширяют диапазон за пределы платформенных дефолтов):** Swiss/International Typographic Style, Müller-Brockmann *Grid Systems*, Vignelli *Canon*, brutalist/editorial web, motion-craft (Material/Apple motion как *намерение*).

**Уровень C — продукты с точкой зрения (изучать ПРИНЦИП, не копировать вид):** Linear (мнение-как-дефолт снижает цену выбора), Arc/Browser Company («налог на новизну»), Things/Cultured Code (крафт-как-вычитание), Teenage Engineering (ограничения как фича), Superhuman (воспринимаемая скорость как материал), Duolingo (мотивация на названной психологии + этический caveat), Monzo/Revolut/Robinhood (личность внутри доверия), Headspace/Calm (темп как материал), Spotify Wrapped (data-storytelling).

**Генеративный метод (новая способность — выводить, а не доставать; запускается ПОСЛЕ заземления на иерархию доказательств):**
1. **Переформулируй работу (JTBD):** «Когда [ситуация], я хочу [мотивация], чтобы [исход]».
2. **Открой вопрос (How Might We):** 2–3 HMW из работы.
3. **Разойдись быстро (Crazy Eights):** 8 направлений за 8 минут — против «первой-идеи».
4. **Впрысни вынужденный вход (de Bono Random Entry / «Po»):** случайное слово / принцип из Уровня C / школа из Уровня B + одна провокация.
5. **Трансформируй базу (SCAMPER):** Substitute/Combine/Adapt/Modify/Put-to-use/Eliminate/Reverse.
6. **Кросс-отраслевая аналогия:** заимствуй *механизм* из не-конкурента, не хром.
7. **Сойдись на 2–3 направлениях**, назови тезисом, не муд-бордом.
8. **Переведи в механизм (обязательный шаг):** spacing/grid-отношение, плотность с причиной, type-роли, motion-намерение + reduced-motion, один композиционный ход, токены цвета, охват состояний.
9. **Пере-сверься с иерархией доказательств** (контраст, масштаб текста, тач-таргеты, восстановление навигации, платформа).

**Дисциплина «референс → механизм»:** референс не воспроизводится, а раскладывается на механизм (воздушность → spacing-отношение; «премиум»-плотность → явный выбор плотности с причиной; motion → намерение+тайминг+fallback; раскладка → один композиционный ход). Источник-опора: NN/g «Competitive Usability Evaluations» («бей конкурента, а не копируй») и «7 Steps to Benchmark UX» (бенчмарк = метрика, не дизайн-для-копии).

**Куда встраивать:** `docs/inspiration-sources.md` (уровни A/B/C + метод, гейт и чеклист сохранить), `docs/visual-benchmark-playbooks.md` (две NN/g-ссылки), `docs/sources.md` (de Bono/SCAMPER/JTBD в подраздел «Creative methods»).

---

## 8. Полный пример: ревью ДО и ПОСЛЕ апгрейда

Один и тот же экран — профиль-форма из `examples/review-screen.md` (D2, текст). Показаны 2 находки из ~8, блок баллов и Bold move — чтобы разница была видна, без полного простыня.

### ДО (текущий стиль — «плавает»)

```md
## Usability issues
- The form is too long without visible grouping, which increases scanning effort.
- Required fields are discovered too late, which encourages preventable errors.
## Design quality issues
- Current design quality score: 2/5 — provisional structural score from text-only input.
## Recommended fixes
- Group fields into sections such as Personal, Contact, Work, and Address.
- Mark required fields before submission.
```
*Проблема: «сгруппируй поля» и «слишком длинная форма» — в разных секциях, связь домысливается; что это даст — не сказано; куда поедет балл — неизвестно.*

### ПОСЛЕ (новый стиль — причинно, с прогнозом, со смелым ходом)

```md
## Findings
### F1 — Required fields revealed only at submit
- Lens: Usability
- Observation: Required fields are not marked until the user submits.
- Violated principle: Nielsen #5 Error prevention; Wroblewski form-design (mark required up front).
- User consequence: Older enterprise users fill the whole form, hit submit, then back-track to fix errors — high-effort recovery on a long form.
- Change: Mark required fields inline before submit; validate on blur with supportive helper text.
- Predicted effect: Should cut submit-time error bounce on this form; confidence M (D2 text-only — structural inference, not measured).
- Severity: 3 (major) — frequent (every submit), high impact (rework), persistent (repeats each edit).
- Moves: Production readiness 2→3; lifts cap: none (incremental).

### F2 — Flat, ungrouped long form
- Lens: Hierarchy & readability
- Observation: 8 fields share one visual block with no sectioning.
- Violated principle: Gestalt proximity / common region; Cognitive load (extraneous).
- User consequence: User parses the whole form as one undifferentiated list, slowing scanning and increasing perceived length — worse with large text.
- Change: Group into Personal / Contact / Work / Address with section headers.
- Predicted effect: Should reduce scanning effort and perceived length; confidence M.
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path 2→3, Composition 2→4.

## Design quality score (current → projected)
- Current: 2/5 — provisional (D2 text-only); pinned by late-required-fields (P1-class) + placeholder-as-label.
- Projected: 3/5 — median of the assessable dimensions once F1–F3 land; conditional on those fixes. Provisional (D2): visual dimensions stay n/v.
- Ceiling note: with a visual pass confirming contrast/spacing/large-text, the ceiling is 4/5 (resilience such as dark mode and AT semantics still unverified from description).
- Primary lever(s): F1 (lifts the P1 cap pinning the score at 2).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 2 | 3 | rung 2→3 (F2) | provisional |
| Production readiness | 2 | 3 | F1 lifts P1 cap | provisional |
| Composition & spacing | n/v | n/v | not verifiable from text | not-from-text |
| Color, state & contrast | n/v | n/v | not verifiable from text | not-from-text |
- Projected overall = median of the assessable (non-n/v) dimensions {3, 3} = 3. Visual dimensions are not projected upward from text.

## Bold move
- This 2/5 screen has unresolved severity-3 findings, so the trigger is NOT met — the real review defers the Bold move and fixes the foundation first. The block below is shown only to illustrate the Bold-move shape; it would appear once the screen is competent and inert:
  - The move: Split the 8-field form into a 3-step progressive flow (Personal → Contact → Work) with a persistent save.
  - Deviates from: the product's "everything on one screen" edit model.
  - Job served (JTBD): "When I update my profile occasionally, I want to finish without re-checking what I missed, so I can trust my data is correct." Outcome: minimize the number of fields visible at once while keeping completion obvious.
  - UX upside: Cuts per-screen cognitive load (Miller/Hick), makes required-field recovery local, fits one-handed older-user use.
  - Risk / cost: More taps; power users lose the single-scroll edit; dev cost of step state + partial save.
  - De-risk / validate: Prototype A/B vs. grouped single form on completion rate + error rate; kill if completion drops. Must still pass large-text + focus-order checks.
- Score impact: safe fixes (grouped single form) → 4/5; this stepped flow targets 5/5 on resilience but does NOT raise the score until validated.
- Conviction: Worth a spike.
```

Разница буквально измеримая: каждый Finding — самодостаточная цепочка; балл показывает «откуда и куда и при каких условиях»; смелый ход, противоречащий продуктовой модели «всё на одном экране», предложен честно — с работой, апсайдом, ценой и планом проверки.

---

## 9. План внедрения по файлам

Фазированно, от высокого рычага к калибровке. Оценки трудозатрат — порядковые.

**Фаза A — Ядро (закрывает требования 1–3). ~ полдня.**
- `skill/templates.md` — заменить секции проблем/фиксов на блок **Findings**; заменить строку балла на блок **score (current→projected)**; добавить блок **Bold move**.
- `skill/modes.md` — обновить «Output structure» и «Validation checklist» Mode D под новые блоки; переименовать Mode D в «expert review» с заметкой о смеси «критика+аудит».
- `docs/design-quality-rubric.md:44-48` — правило вывода: оба балла + условная грамматика.
- `docs/self-review.md` — 4 новые проверки Mode D (цепочка, сирота, эффект, придержанный смелый ход).

**Фаза B — Доказательная база и креатив. ~ полдня.**
- `docs/heuristics.md` + `docs/sources.md` — Cognitive Load (Sweller), Web Form Design (Wroblewski), Laws of UX, шкала severity Нильсена, NN/g actionable findings, distinctiveness-фреймворки.
- `docs/design-quality.md` + рубрика — 7 креативных рычагов + тест «безликого экрана».
- `docs/guardrails.md` + `examples/anti-patterns.md` — карваут для Bold move + пара Bad/Good.

**Фаза C — Калибровка (иначе модель воспроизведёт старый формат). ~ полдня.**
- `examples/review-screen.md` + `examples/golden/settings.md` — перегенерить в новый формат (это де-факто спецификация — модель копирует пример надёжнее, чем парсит шаблон).
- `examples/visual-review-fixtures/*` — добавить ожидаемый current **и** projected балл.
- `docs/evals.md` — checks: условная грамматика, потолок 4/5, provisional D2/D3, нет числа при Fail, фикс называет принцип+эффект.

**Фаза D — Inspiration v2.**
- `docs/inspiration-sources.md` (уровни A/B/C + генеративный метод), `docs/visual-benchmark-playbooks.md` (NN/g-ссылки).

---

## 10. Риски и как их снять

| Риск | Снятие |
|---|---|
| **Раздувание / «process theater»** (нарушает собственную слабость №12 скилла) | Блок Finding *заменяет* две секции, а не добавляет; Low-severity сжимается до 3 полей; таблица баллов — 8 строк, строки без изменений схлопываются в «—». Мы реструктурируем, а не наращиваем. |
| **Инфляция балла / ложная точность** | Условная грамматика обязательна; дельта по медиане, не сумме; потолок 4/5; кэпы снимаются только по условию; eval ловит голое after-число. |
| **Визуальный overclaim через прогноз (D2/D3)** | Визуальные измерения не прогнозируются вверх, уходят в Unresolved assumptions; весь прогноз — «дважды provisional». |
| **Bold move как лазейка для эстетической отмывки** | Карантин после фиксов; 8 обязательных полей; запрещён в Severity/фиксах; не может отменить фикс; держится на *более высокой* планке (нужны JTBD-работа + измеримый исход + план проверки + kill-критерий). |
| **Смелый ход на сломанном экране** | Триггер: нет неустранённой находки severity 3–4 и экран уже ≥3/5. Сначала фундамент. |
| **Потеря лучшей черты (дисциплина D1–D4)** | Все новые слои живут *внутри* суб-кейсов; новый прогностический слой явно наследует границы доказательств. |

---

## 11. Источники (проверены в ходе ресёрча)

**Критика, оценка, severity:** Nielsen «Severity Ratings for Usability Problems» (NN/g, 1994); Connor & Irizarry, *Discussing Design* (O'Reilly, 2015); Schade «Making Usability Findings Actionable» (NN/g, 2013); Knapp, *Sprint* (GV). **Принципы «почему»:** Nielsen 10 Heuristics; Yablonski, *Laws of UX* (2020); Sweller, Cognitive Load Theory (1988); Wroblewski, *Web Form Design* (2008); Gestalt (NN/g). **Before/after:** Sauro & Lewis, *Quantifying the UX* (2016, SUS); Sullivan «Hypothesis Kit»; PIE/RICE/ICE (Goward; Intercom/McBride; Ellis). **Креатив/отличительность:** Neumeier, *Zag* (2007); Sharp & Romaniuk, *Building Distinctive Brand Assets* (2018); Kano et al. (1984); Norman, *Emotional Design* (2004); Walter, *Designing for Emotion* (2011); Anderson, *Seductive Interaction Design* (2011); Kholmatova, *Design Systems* (2017); Val Head, *Designing Interface Animation* (2016); Thomas & Johnston, *The Illusion of Life* (Disney 12, 1981); Lupton, *Thinking with Type* (2010). **Смелый ход:** JTBD (Christensen; Ulwick, 2016; Moesta); Dunne & Raby, *Speculative Everything* (2013); Rams, Ten Principles. **Метод/источники:** d.school Design Thinking Bootleg; Crazy Eights (Google Design Sprint Kit); de Bono, Lateral Thinking; SCAMPER (Eberle/Osborn); NN/g «Competitive Usability Evaluations» и «7 Steps to Benchmark UX»; Airbnb DLS; The Linear Method; Stripe/Figma/Intercom/Spotify/Polaris design writing.

> Пометки честности из ресёрча: эмпирический статус Neumeier — практик-аргумент, не соц.наука (нести как дисциплину решения, не как доказательство); конкретный бюджет ≤1/≤2 — предложенный дефолт, не число Kholmatova; «provotype» как термин Dunne & Raby — `[unverified]`. Остальное сверено с источниками.
