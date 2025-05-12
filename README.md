# pythonKursova
1 стъпка - Изтегли git
2 стъпка - влизаш в папка за курсовата, напр. pythonkursova и отваряш cmd за нея 
3 стъпка - Пишеш git init, git pull https://github.com/ivaylaDim/pythonKursova.git, това тегли всички файлове от main бранча до момента
4 стъпка - Влизаш във Visual Studio Code и добавяш папката към workspace
5 стъпка - В горния ляв ъгъл трябва да има terminal, отваряш го за текущата папка
6 стъпка - В терминала пишеш git init отново, за всеки случай. След това git remote add origin https://github.com/ivaylaDim/pythonKursova.git
7 стъпка - Пишеш git checkout salihcan, след това git pull https://github.com/ivaylaDim/pythonKursova.git, след това git push --set-upstream origin salihcan (това те мести в отделен бранч, който не влияе на главния)
8 стъпка - Когато правиш промени пишеш git add . (с точката), след това git commit, пишеш в текст едитора каква е новата промяна и го затваряш с х. След това git push за да се добави новия код в репото.
9 стъпка - Преди да се слее новия код от github се прави pull request/merge request . След това се слива в мастер.
