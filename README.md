# data-pipeline
Minimum viable DataFrame pipeline.


## Usage

```python
df = pd.DataFrame({'a': [1, 2, 3, 4, -1]})
pipeline = Pipeline([__LogShape('Initial shape:'),
                     TransformCol('a', lambda x: x * 2),
                     ExprAssign('b', 'a+1'),
                     ExprAssign('a', 'a-1'),
                     Filter('b', lambda x: x > 5),
                     __LogShape('After filtering for b:'),
                     ResetIndex(),
                     __Log('Done.')
                     ])
pipeline.apply(df)
          
Initial shape: (5, 1)
After filtering for b: (2, 2)
Done.
   a  b
0  5  7
1  7  9
 
```
