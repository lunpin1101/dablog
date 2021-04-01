# dablog

A **D**eep **A**utoencoder-**B**ased Anoamly Detection Method for Discrete Event **Log**s

[Lun-Pin Yuan, Peng Liu, and Sencun Zhu, *"Recomposition vs. Prediction: A Novel Anomaly Detection for Discrete Events Based On Autoencoder"*](https://arxiv.org/abs/2012.13972)

# Description

<p> This is a placeholder for the project. I will update this repository soon. </p>

# Examples

Please refer to the paper for parameters.

```
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k706_ip1hr -m deeplog --window-size 60 --key-divisor 100 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k706_ip1hr -m dablog --window-size 60 --key-divisor 100  ; \
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k706_iphhr -m deeplog --window-size 30 --key-divisor 100 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k706_iphhr -m dablog --window-size 30 --key-divisor 100  ; \
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k706_ipqhr -m deeplog --window-size 15 --key-divisor 100 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k706_ipqhr -m dablog --window-size 15 --key-divisor 100  ; \
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k366_ip1hr -m deeplog --window-size 60 --key-divisor 1000 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k366_ip1hr -m dablog --window-size 60 --key-divisor 1000  ; \
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k366_iphhr -m deeplog --window-size 30 --key-divisor 1000 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k366_iphhr -m dablog --window-size 30 --key-divisor 1000  ; \
exp-unswnb15.py ad -o out/2020-10-21_deeplog_k366_ipqhr -m deeplog --window-size 15 --key-divisor 1000 ; \
exp-unswnb15.py ad -o out/2020-10-21_dablog_k366_ipqhr -m dablog --window-size 15 --key-divisor 1000  ; \
```
