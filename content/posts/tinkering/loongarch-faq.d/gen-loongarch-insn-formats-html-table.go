package main

import (
	"fmt"
	"os"
	"sort"

	"github.com/loongson-community/loongarch-opcodes/scripts/go/common"
)

func main() {
	inputs := os.Args[1:]

	descs, err := common.ReadInsnDescs(inputs)
	if err != nil {
		panic(err)
	}

	formats := gatherFormats(descs)

	sort.Slice(descs, func(i int, j int) bool {
		return descs[i].Word < descs[j].Word
	})

	sort.Slice(formats, func(i int, j int) bool {
		return formats[i].CanonicalRepr() < formats[j].CanonicalRepr()
	})

	emitInsnFormatTypes(formats)
}

////////////////////////////////////////////////////////////////////////////

func gatherFormats(descs []*common.InsnDescription) []*common.InsnFormat {
	formatsSet := make(map[string]*common.InsnFormat)
	for _, d := range descs {
		canonicalFormatName := d.Format.CanonicalRepr()
		if _, ok := formatsSet[canonicalFormatName]; !ok {
			formatsSet[canonicalFormatName] = d.Format
		}
	}

	result := make([]*common.InsnFormat, 0, len(formatsSet))
	for _, f := range formatsSet {
		result = append(result, f)
	}

	return result
}

////////////////////////////////////////////////////////////////////////////

type fieldTd struct {
	msb      int
	colspan  int
	isOpcode bool
	name     string
}

func detectOpcodeFields(matchMask uint32) []fieldTd {
	var result []fieldTd
	var currFieldLSB int
	var currFieldMSB int
	var scanningOpcodeField bool

	i := 0
	for matchMask != 0 {
		currBit := matchMask & 1
		matchMask >>= 1
		i++

		if currBit != 0 {
			if !scanningOpcodeField {
				scanningOpcodeField = true
				currFieldLSB = i
			}

			currFieldMSB = i
			continue
		}

		// saw operand
		if scanningOpcodeField {
			result = append(result, fieldTd{
				msb:      currFieldMSB,
				colspan:  currFieldMSB - currFieldLSB + 1,
				isOpcode: true,
				name:     "",
			})
		}
		scanningOpcodeField = false
	}

	if scanningOpcodeField {
		result = append(result, fieldTd{
			msb:      currFieldMSB,
			colspan:  currFieldMSB - currFieldLSB + 1,
			isOpcode: true,
			name:     "",
		})
	}

	return result
}

var argNameMap = map[string]string{
	"D":  "rd",
	"J":  "rj",
	"K":  "rk",
	"A":  "ra",
	"Fd": "fd",
	"Fj": "fj",
	"Fk": "fk",
	"Fa": "fa",
	"Cd": "cd",
	"Cj": "cj",
	"Ck": "ck",
	"Ca": "ca",
}

func emitInsnFormatTypes(fmts []*common.InsnFormat) {
	for _, f := range fmts {
		fmt.Printf("        <tr><td>%s</td>", f.CanonicalRepr())

		// for detecting disjoint opcode fields
		fieldCells := detectOpcodeFields(f.MatchBitmask())

		// add args
		for _, a := range f.Args {
			argRepr := a.CanonicalRepr()
			if repl, ok := argNameMap[argRepr]; ok {
				// argRepr = repl
				_ = repl
			}

			for slotIdx, s := range a.Slots {
				var repr string
				if len(a.Slots) == 1 {
					repr = argRepr
				} else {
					var part string
					if slotIdx == 0 {
						part = "高位"
					} else {
						part = "低位"
					}
					repr = fmt.Sprintf("%s %s", argRepr, part)
				}

				fieldCells = append(fieldCells, fieldTd{
					msb:      int(s.MSB()),
					colspan:  int(s.Width),
					isOpcode: false,
					name:     repr,
				})
			}
		}

		sort.Slice(fieldCells, func(i int, j int) bool {
			return fieldCells[i].msb > fieldCells[j].msb
		})
		for _, td := range fieldCells {
			fmt.Printf(`<td `)
			if td.isOpcode {
				fmt.Printf(`class="field-opcode" `)
			}
			fmt.Printf(`colspan="%d">%s</td>`, td.colspan, td.name)
		}
		fmt.Printf("</tr>\n")
	}
}
