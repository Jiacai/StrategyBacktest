package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
	"strconv"
	"math"
	"sort"
	// "math/rand"
	// "time"
)

const CAPE_BASE = 30.54
const PRICE_BASE = 3141.26

func run(PC95, PC90, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 float64, CAPE_LST []float64, sample_map map[int][]map[string]float64) float64 {
	
	// how to calculate temperature
	// fmt.Println(cape_lst)
	// i := sort.Search(len(cape_lst), func(i int) bool { return cape_lst[i] >= 20 })
	// fmt.Println(float64(i) / float64(len(cape_lst)))
	
	win_count := 0
	const SAMPLE_COUNT = 10
	for i := 0; i < SAMPLE_COUNT; i++ {
		// we need to make sure not side effect to operate on the same data map
		data := sample_map[i]
		tmp_lst := make([]float64, len(CAPE_LST))
		copy(tmp_lst, CAPE_LST)
		position := 0.0
		rtn := 0.0
		price := 0.0
		cum_rtn := 0.0
		// process data
		idx := 0
		for _, row := range data {
			// process return
			if price != 0.0 {
				rtn = math.Log(row["price"] / price)
			}

			price = row["price"]

			cum_rtn = cum_rtn + (rtn * position)
			// fmt.Println(cum_rtn)
			cape := row["cape"]

			rank := sort.Search(len(tmp_lst), func(i int) bool { return tmp_lst[i] >= cape })

			pct := float64(rank) / float64(len(tmp_lst))
			// round to 4 decimal
			pct = math.Round(pct * 10000) / 10000

			tmp_lst = append(tmp_lst, cape)
			sort.Float64s(tmp_lst)

			// // debug:
			// if idx == 138 {
			// 	fmt.Println(price, cape, pct, position, rtn, cum_rtn)
			// }

			row["cape_pct"] = pct
			if pct >= 0.95 {
				position = PC95
			} else if pct >= 0.9 {
				position = PC90
			} else if pct >= 0.8 {
				position = PC8
			} else if pct >= 0.7 {
				position = PC7
			} else if pct >= 0.6 {
				position = PC6
			} else if pct >= 0.5 {
				position = PC5
			} else if pct >= 0.4 {
				position = PC4
			} else if pct >= 0.3 {
				position = PC3
			} else if pct >= 0.2 {
				position = PC2
			} else if pct >= 0.1 {
				position = PC1
			} else {
				position = PC0
			}

			row["position"] = position
			idx += 1
		}

		nav := math.Exp(cum_rtn)
		if nav > (price / PRICE_BASE) {
			win_count += 1
		}
	}
	fmt.Println(float64(win_count) / float64(SAMPLE_COUNT))
	return float64(win_count) / float64(SAMPLE_COUNT)
	
}

func main() {
	// LOAD cape file
	capefile, err := os.Open("data/cape.txt")
	if err != nil {
		panic(err)
	}

	defer capefile.Close()
	CAPE_LST := []float64{}
	creader := bufio.NewReader(capefile)

	for {
		line, _, err := creader.ReadLine()

		if err == io.EOF {
			break
		}
		cape, _ := strconv.ParseFloat(string(line), 64)
		CAPE_LST = append(CAPE_LST, cape)
	}
	CAPE_LST = CAPE_LST[:756]
	// let's sort it for easy ranking
	sort.Float64s(CAPE_LST)


	// LOAD sample map
	sample_map := map[int][]map[string]float64{}
	for i := 0; i < 10; i++ {
		samplefile, err := os.Open(fmt.Sprint("sample/sample_", i, ".csv"))
		if err != nil {
			panic(err)
		}

		defer samplefile.Close()

		data := []map[string]float64{}

		sreader := bufio.NewReader(samplefile)

	    cum_mood := 0.0
	    cum_price := 0.0

		for {
			line, _, err := sreader.ReadLine()

			if err == io.EOF {
				break
			}

			s := strings.Split(string(line), ",")
			if s[0] != "alpha" {
				m := make(map[string]float64)
				m["_alpha"], _ = strconv.ParseFloat(s[0], 64)
				m["_mood"], _ = strconv.ParseFloat(s[1], 64)
				m["_price"], _ = strconv.ParseFloat(s[2], 64)
				cum_mood += m["_mood"]
				cum_price += m["_price"]
				m["cape"] = math.Exp(cum_mood) * CAPE_BASE
				m["price"] = math.Exp(cum_price) * PRICE_BASE 
				data = append(data, m)
			}
		}
		sample_map[i] = data
	}


	// PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 := 0.2, 0.9, 0.8, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0
	// PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 := 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    // for i := 5; i < 30; i++ {
    base_rate := 0.0
    f, err := os.Create("params.txt")
    defer f.Close()
    datawriter := bufio.NewWriter(f)
    // s := rand.NewSource(time.Now().UnixNano())
    // r := rand.New(s)
    // for i := 0; i < 1000; i++ {
    // 	a := r.Float64()
    // 	b := r.Float64()
    // 	// a <= b
    // 	if a > b {
    // 		a, b = b, a
    // 	}
    // 	if a > 0.05 || b < 0.65 {
    // 		continue
    // 	}
    // }
    for i := 0; i < 6; i++ {
    	for j := 0; j < 6; j++ {
    		a := float64(i) * 0.01
    		b := float64(j) * 0.01 + 0.67
    		_PC95 := a
	    	_PC90 := b
	        // _PC9 := float64(i) * 0.01 + 0.0
	        _PC5, _PC6, _PC7, _PC8 := 1.0, 1.0, 1.0, 1.0
	        _PC0, _PC1, _PC2, _PC3, _PC4 := 1.0, 1.0, 1.0, 1.0, 1.0
	        fmt.Println(_PC95, _PC90, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0)
	        rate := run(_PC95, _PC90, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0, CAPE_LST, sample_map)
	        if rate > base_rate {
	        	fmt.Println("!IMPROVED!")
	        	base_rate = rate
	        	line := fmt.Sprint("[", _PC95, _PC90, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0, "] rate:", rate)
	        	_, _ = datawriter.WriteString(line + "\n")
	        	datawriter.Flush()
	        	f.Sync()
	        }
    	}
    }

	// for _, row := range data {
	// 	fmt.Println(row["mood"], row["price"])
	// }
}
