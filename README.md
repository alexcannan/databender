# getbent

databending using python

Inspired by https://www.hellocatfood.com/databending-using-audacity/

## μ-law Encoding

To match the behavior of the original blog post, special care should be taken to match the `U-LAW` and `Big-Endian` settings used during import and export. In practical terms we simply need to map every byte to a value between -1 and 1 using a special curve defined by [μ-law Encoding](https://en.wikipedia.org/wiki/%CE%9C-law_algorithm).