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

// this is for another project, but the way to fast iteration is illustrated here

const PE_BASE = 34.20517103
const PRICE_BASE = 4186.18

func run(PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 float64, PE_LST []float64, sample_map map[int][]map[string]float64) float64 {
	
	win_count := 0
	const SAMPLE_COUNT = 100
	for i := 0; i < SAMPLE_COUNT; i++ {
		// we need to make sure not side effect to operate on the same data map
		data := sample_map[i]
		tmp_lst := make([]float64, len(PE_LST))
		copy(tmp_lst, PE_LST)
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
			pe := row["pe"]

			rank := sort.Search(len(tmp_lst), func(i int) bool { return tmp_lst[i] >= pe })

			pct := float64(rank) / float64(len(tmp_lst))
			// round to 4 decimal
			pct = math.Round(pct * 10000) / 10000

			tmp_lst = append(tmp_lst, pe)
			sort.Float64s(tmp_lst)


			row["cape_pct"] = pct
			if pct >= 0.9 {
				position = PC9
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
	capefile, err := os.Open("data/pe_new.txt")
	if err != nil {
		panic(err)
	}

	defer capefile.Close()
	PE_LST := []float64{}
	creader := bufio.NewReader(capefile)

	for {
		line, _, err := creader.ReadLine()

		if err == io.EOF {
			break
		}
		cape, _ := strconv.ParseFloat(string(line), 64)
		PE_LST = append(PE_LST, cape)
	}
	// let's sort it for easy ranking
	sort.Float64s(PE_LST)


	// LOAD sample map
	sample_map := map[int][]map[string]float64{}
	for i := 0; i < 1000; i++ {
		samplefile, err := os.Open(fmt.Sprint("sample2/sample_", i, ".csv"))
		if err != nil {
			panic(err)
		}

		// defer samplefile.Close()

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
				m["pe"] = math.Exp(cum_mood) * PE_BASE
				m["price"] = math.Exp(cum_price) * PRICE_BASE 
				data = append(data, m)
			}
		}
		sample_map[i] = data
		samplefile.Close()
	}


	// PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 := 0.2, 0.9, 0.8, 0.7, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0
	// PC9, PC8, PC7, PC6, PC5, PC4, PC3, PC2, PC1, PC0 := 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    // for i := 5; i < 30; i++ {
    base_rate := 0.0
    f, err := os.Create("params.txt")
    defer f.Close()
    datawriter := bufio.NewWriter(f)
    pos_lst := []float64{0.0, 0.65, 0.72, 0.9, 0.95, 0.95, 0.97, 0.98, 0.99, 1.0}
	for k := 7; k < 10; k++ {
		// s := rand.NewSource(time.Now().UnixNano())
  //   	r := rand.New(s)
		lower_b := 0.0
		higher_b := 1.0
		if k != 0 {
			lower_b = pos_lst[k - 1]
			lower_b = math.Round(lower_b * 100) / 100
		}
		if k != 9 {
			higher_b = pos_lst[k + 1]
			higher_b = math.Round(higher_b * 100) / 100
		}
		for a := lower_b; a < higher_b; a += 0.01 {
			a = math.Round(a * 100) / 100
			local_pos_lst := make([]float64, len(pos_lst))
			copy(local_pos_lst, pos_lst)
			local_pos_lst[k] = a

			_PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0 := local_pos_lst[0], local_pos_lst[1], local_pos_lst[2], local_pos_lst[3], local_pos_lst[4], local_pos_lst[5], local_pos_lst[6], local_pos_lst[7], local_pos_lst[8], local_pos_lst[9] 

		    fmt.Println(_PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0)
		    rate := run(_PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0, PE_LST, sample_map)
		    if rate >= base_rate {
		    	line := fmt.Sprint("[", _PC9, _PC8, _PC7, _PC6, _PC5, _PC4, _PC3, _PC2, _PC1, _PC0, "] rate:", rate)
		    	_, _ = datawriter.WriteString(line + "\n")
		    	datawriter.Flush()
		    	f.Sync()
		    	if rate > base_rate {
			    	fmt.Println("!IMPROVED!")
			    	base_rate = rate
			    	
					// pos_lst := make([]float64, len(local_pos_lst))
					copy(pos_lst, local_pos_lst)
				}
		    }
		}
		
	}

	// for _, row := range data {
	// 	fmt.Println(row["mood"], row["price"])
	// }
}

