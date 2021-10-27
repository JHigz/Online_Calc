output "output_webserver_ip_address" {
  value = aws_instance.cyber94_jhiguita_calculator_2_webserver_tf.*.public_ip
}
