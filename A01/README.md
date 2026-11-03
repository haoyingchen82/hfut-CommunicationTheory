
# A01

## 1. 题目模型

已知随机过程：

\[
z(t)=m(t)\cos(\omega_0t+\theta)
\]

其中：

- \(m(t)\) 为广义平稳随机过程；
- \(\theta\sim U(0,2\pi)\)；
- \(\theta\) 与 \(m(t)\) 统计独立。

原随机过程的自相关函数为：

\[
R_m(\tau)=
\begin{cases}
1-|\tau|,&|\tau|<1\\
0,&\text{其他}
\end{cases}
\]

## 2. 数学推导

### 2.1 证明广义平稳性

首先求均值：

\[
E[z(t)]
=
E[m(t)\cos(\omega_0t+\theta)]
\]

利用统计独立性：

\[
E[z(t)]
=
E[m(t)]E[\cos(\omega_0t+\theta)]
\]

由于随机变量 \(\theta\) 服从均匀分布：

\[
E[\cos(\omega_0t+\theta)]
=
\frac{1}{2\pi}
\int_0^{2\pi}
\cos(\omega_0t+\theta)d\theta
=0
\]

因此：

\[
\boxed{E[z(t)]=0}
\]

接下来求自相关函数：

\[
R_z(t_1,t_2)
=
E[z(t_1)z(t_2)]
\]

代入：

\[
\begin{aligned}
R_z(t_1,t_2)
=&E[m(t_1)m(t_2)\\
&\cdot\cos(\omega_0t_1+\theta)\\
&\cdot\cos(\omega_0t_2+\theta)]
\end{aligned}
\]

利用统计独立性：

\[
\begin{aligned}
R_z(t_1,t_2)
=&R_m(t_1-t_2)\\
&\cdot E[
\cos(\omega_0t_1+\theta)
\cos(\omega_0t_2+\theta)]
\end{aligned}
\]

利用积化和差公式：

\[
\cos A\cos B
=
\frac12[\cos(A-B)+\cos(A+B)]
\]

对均匀分布的随机相位求期望：

\[
E[\cos(A+B)]=0
\]

因此：

\[
E[\cos A\cos B]
=
\frac12\cos(A-B)
\]

最终：

\[
\boxed{
R_z(\tau)
=
\frac12R_m(\tau)\cos(\omega_0\tau)
}
\]

由于均值为常数，自相关函数只与时间差有关，因此：

\[
\boxed{z(t)\text{ 是广义平稳随机过程}}
\]

### 2.2 求自相关函数

将题目给出的 \(R_m(\tau)\) 代入：

\[
R_z(\tau)=
\begin{cases}
\frac12(1-|\tau|)\cos(\omega_0\tau),
&|\tau|<1\\
0,&\text{其他}
\end{cases}
\]

### 2.3 求功率谱密度

采用傅里叶变换定义：

\[
P_z(f)=
\int_{-\infty}^{+\infty}
R_z(\tau)e^{-j2\pi f\tau}d\tau
\]

首先求原随机过程的功率谱密度：

\[
P_m(f)=
\mathcal F\{R_m(\tau)\}
\]

利用三角函数的傅里叶变换：

\[
\boxed{P_m(f)=\operatorname{sinc}^2(f)}
\]

其中：

\[
\operatorname{sinc}(x)=
\frac{\sin(\pi x)}{\pi x}
\]

令：

\[
f_0=\frac{\omega_0}{2\pi}
\]

根据傅里叶变换的频移性质：

\[
\mathcal F\{R_m(\tau)\cos(2\pi f_0\tau)\}
=
\frac12[
P_m(f-f_0)+P_m(f+f_0)]
\]

因此：

\[
\boxed{
P_z(f)=\frac14
\left[
\operatorname{sinc}^2(f-f_0)
+
\operatorname{sinc}^2(f+f_0)
\right]
}
\]

### 2.4 求平均功率

根据自相关函数的定义：

\[
S=E[z^2(t)]=R_z(0)
\]

代入：

\[
S=\frac12(1-0)\cos(0)
\]

最终：

\[
\boxed{S=\frac12}
\]

## 3. 工程结构

```text
A01/
├── README.md
├── main.py
├── model.py
├── visualization.py
└── outputs/
    └── a01_visualization.png
```

文件职责：

- `main.py`：程序入口，负责参数解析与执行流程。
- `model.py`：负责数学模型、自相关函数、功率谱密度和平均功率计算。
- `visualization.py`：负责绘制统计特征曲线并保存图片。
- `README.md`：记录题目背景、数学推导和运行说明。
- `outputs/`：保存最终可视化结果。

## 4. 运行方法

在 Assignments 根目录执行：

```powershell
uv run python A01/main.py
```

默认载波角频率：

\[
\omega_0=2\pi\ \mathrm{rad/s}
\]

指定载波角频率：

```powershell
uv run python A01/main.py --omega0 12.5663706144
```

指定图片输出位置：

```powershell
uv run python A01/main.py --output A01/outputs/result.png
```

## 5. 输出结果

程序生成：

```text
A01/outputs/a01_visualization.png
```

图片依次展示：

1. 原随机过程的自相关函数。
2. 调制后随机过程的自相关函数及其包络。
3. 调制后随机过程的功率谱密度。

