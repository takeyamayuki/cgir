# 概要
Raspberry Piで赤外線送受信、データ解析をするPythonライブラリとコマンドラインツールです。
- cgir.py : pigpioを使って赤外線の送受信、データ解析をするモジュール
- cgirtool.py : 赤外線送受信、データ解析をコマンドラインから使用できるようにしたツール

# 使い方
コマンドラインツールの使い方は`./cgirtool.py -h`もしくは[解説記事](https://www.indoorcorgielec.com/resources/raspberry-pi/python-pigpio-infrared)を参照して下さい。

# 対応ハードウェア
[circuit](circuit)リポジトリに回路図を示す


# 前準備
## pigpioサービス
`sudo service pigpiod start`

`sudo systemctl enable pigpiod.service`

## docoptモジュール
`sudo pip3 install docopt`

# 送信しても機器が反応しない場合
一部環境で、pigpioのクロックソースがPCMの場合、意図した周波数にならず送信に失敗(機器が反応しない)する現象を確認しています。その場合は以下をお試しください。

スーパーユーザーで /lib/systemd/system/pigpiod.service ファイルを開き、ExecStart行の最後に「-t 0」を追加します。編集後にRasbperry Piを再起動します。

`ExecStart=/usr/bin/pigpio -l -t 0`
