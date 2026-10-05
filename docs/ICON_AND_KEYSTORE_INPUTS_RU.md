# Входы для правил иконок и всех keystore-форматов

Правила FILE/FOLDER, EXACT/GLOB/REGEX, project/global и priority раскрыты в
[DEV-04](ALL_FUNCTIONS_RU.md#dev-04). Для submodule-only нужен настоящий Git
gitlink. Из корня demo создайте новую независимую копию:

```powershell
python -B -X utf8 suite-support/prepare_icon_submodule.py --output D:/CodexData/Temp/archverity-icon-demo
```

Откройте этот output как IDEA project. `demo-icon-module` — действительный
локальный submodule с index mode `160000`; `payment-app` — обычная папка.
Создайте FOLDER/EXACT rule с pattern `demo-icon-module`, существующим icon ID
и `gitSubmoduleOnly=true`. Для отрицательного случая используйте `payment-app`
с тем же флагом; затем отключите его и проверьте обычное folder rule.
Helper отказывается перезаписывать существующий output. Исходный проект demo
остаётся чистым; содержимое child repository ограничено публичным README.

[KEY-01](ALL_FUNCTIONS_RU.md#key-01) использует семь готовых файлов
`projects/workspace/qa-truststore.{jks,jceks,p12,pfx,bks,bcfks,uber}`.
Demo-пароль всех файлов: `archverity-qa-only`. Каждый содержит ровно один
`archverity-qa` trusted certificate, совпадающий с `qa-cert.der`, без key entries.
Fingerprint: `715d297f1628481a45c647669ef58cb4e30fb8bc7805041128366c2b857551f0`.
Проверьте каждый формат в Keystore/Project View; затем неверный пароль.
Цепочка этого trusted certificate содержит один сертификат. Private/secret-key
entries и многоэлементные private-key chains требуют отдельного разрешённого
операторского input и остаются отдельными NOT RUN cases.

Standalone verifier с JDK 21 проверяет четыре JDK-файла:

```powershell
java suite-support/PublicTruststores.java verify projects/workspace
```

Для всех семи используйте `bcprov-jdk18on-1.85.jar` из своей законно полученной
Tools/plugin development distribution:

```powershell
java --class-path "PATH/TO/bcprov-jdk18on-1.85.jar" suite-support/PublicTruststores.java verify projects/workspace --require-bc
```

Verifier проверяет содержимое, fingerprint и отказ с неверным паролем.
BC-форматы без jar помечаются `NOT_RUN`; plugin UI использует собственный
BC 1.85. Type names сверены с официальным [BC 1.85 mapping](https://github.com/bcgit/bc-java/blob/r1rv85/prov/src/main/java/org/bouncycastle/jcajce/provider/keystore/BC.java)
и [BCFKS mapping](https://github.com/bcgit/bc-java/blob/r1rv85/prov/src/main/java/org/bouncycastle/jcajce/provider/keystore/BCFKS.java).
Зависимости demo для этой проверки не изменены, jar не включён в публичный Git.
