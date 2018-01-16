# installation
1. clone this repo to your local machine
2. `cd CNTK` to go to the root directory
3. install by `pip install -e .` or `pip3 install -e .` 

# documentation
Please check the corresponding code file, and it will be well documented later   
1. clean chinese text
2. standardize chinese text
3. filter out what you don't need
4. all kinds of tokenization functions: text to sentences, sentence to words or text to characters

An example:  
```python
>>> from cntk.tokenizer import text2charlist as tc
>>> rst = tc(["与awd店名", "“叫", u"了   个鸡”配套的还有不少宣   传标语，", "213", "23包括叫3 123个童 子鸡 、和她有一腿等。"])
["与", "awd", "店", "名", "“ ", "叫", "了", "个", "鸡", "” ", "配", "套", "的", "还", "有", "不", "少", "宣", "传", "标", "语", "，", "213", "23", "包", "括", "叫", "3 ", "123", "个", "童", "子", "鸡", "、", "和", "她", "有", "一", "腿", "等", "。"]
>>> print " ".join(t2c("十九大精神进[UNK]万家｜活跃在 牧区 [UNK] 的“马背宣讲队", keep_word="[UNK]"))
十 九 大 精 神 进 [UNK] 万 家 ｜ 活 跃 在 牧 区 [UNK] 的 “ 马 背 宣 讲 队
```
