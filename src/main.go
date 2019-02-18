package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"fmt"
	"strconv"
	"strings"
	"sync"
	"unsafe"

	"github.com/liuzl/fmr"
)

var (
	index    = make(map[string]int)
	mutex    sync.RWMutex
	grammars []*fmr.Grammar
	g        *fmr.Grammar
	info     string
)

//export init_grammar
func init_grammar(s *C.char) int {
	f := C.GoString(s)
	mutex.RLock()
	defer mutex.RUnlock()
	if i, has := index[f]; has {
		g = grammars[i]
		return i
	}

	i := len(grammars)

	var err error
	g, err = fmr.GrammarFromFile(f)
	if err != nil {
		info = fmt.Sprintf("load grammar file %s error: %+v", f, err.Error())
		return -1
	}
	grammars = append(grammars, g)
	index[f] = i
	return i
}

//export get_last_error
func get_last_error() *C.char {
	return C.CString(info)
}

//export extractx
func extractx(i int, l, s *C.char) *C.char {
	if i < 0 || i >= len(grammars) {
		info = fmt.Sprintf("no grammar found with id %s", i)
		return C.CString(`{"error":"no grammar"}`)
	}
	lg := grammars[i]
	line := C.GoString(l)
	start := C.GoString(s)
	trees, err := lg.ExtractMaxAll(line, start)
	if err != nil {
		info = fmt.Sprintf("ExtractMaxAll error: %+v", err)
		return C.CString(`{"error":` + strconv.Quote(err.Error()) + `}`)
	}
	var ret []string
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			info = fmt.Sprintf("Semantic error: %+v", err)
			return C.CString(`{"error":` + strconv.Quote(err.Error()) + `}`)
		} else {
			ret = append(ret, sem)
		}
	}
	//return C.CString("null")
	return C.CString(`[` + strings.Join(ret, ",") + `]`)
}

//export parse
func parse(i int, l, s *C.char) *C.char {
	if i < 0 || i >= len(grammars) {
		info = fmt.Sprintf("no grammar found with id %s", i)
		return C.CString(`{"error":"no grammar"}`)
	}
	lg := grammars[i]
	line := C.GoString(l)
	start := C.GoString(s)
	trees, err := lg.ExtractMaxAll(line, start)
	if err != nil {
		info = fmt.Sprintf("ExtractMaxAll error: %+v", err)
		return C.CString(`{"error":` + strconv.Quote(err.Error()) + `}`)
	}
	var ret []string
	for _, tree := range trees {
		sem, err := tree.Semantic()
		if err != nil {
			info = fmt.Sprintf("Semantic error: %+v", err)
			return C.CString(`{"error":` + strconv.Quote(err.Error()) + `}`)
		} else {
			ret = append(ret, strings.Replace(sem, "\t", " ", -1))
		}
	}
	return C.CString(strings.Join(ret, "\t"))
}

//export frames
func frames(i int, l *C.char) *C.char {
	if i < 0 || i >= len(grammars) {
		info = fmt.Sprintf("no grammar found with id %s", i)
		return C.CString(`{"error":"no grammar"}`)
	}
	lg := grammars[i]
	line := C.GoString(l)
	ret, err := lg.FrameFMR(line)
	if err != nil {
		info = fmt.Sprintf("FrameFMR error: %+v", err)
		return C.CString(`{"error":` + strconv.Quote(err.Error()) + `}`)
	}
	return C.CString(strings.Join(ret, "\t"))
}

//export gofree
func gofree(cs *C.char) {
	C.free(unsafe.Pointer(cs))
}

func main() {
}
