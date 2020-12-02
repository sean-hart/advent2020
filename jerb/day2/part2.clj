; aoc2020 day 2 part 2

(def input-file "input.txt")

(defn is-valid? [line]
  (let [[p1 p2 c password] (rest (re-find #"(\d+)-(\d+) ([a-zA-Z]): ([a-zA-Z]+)" line))
        p1 (- (Integer/parseInt p1) 1)
        p2 (- (Integer/parseInt p2) 1)
        p1-matched (= c (str (get password p1)))
        p2-matched (= c (str (get password p2)))]
    (or (and p1-matched (not p2-matched))
        (and p2-matched (not p1-matched)))))

(defn solution [input-file]
  (with-open [rdr (clojure.java.io/reader input-file)]
    (count (filter is-valid?
                   (line-seq rdr)))))

(print (solution input-file))

