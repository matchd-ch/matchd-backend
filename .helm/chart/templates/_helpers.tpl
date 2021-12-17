{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "matchd-frontend.name" -}}
{{- default .Chart.Name .Values.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "matchd-frontend.fullname" -}}
{{- if .Values.fullname -}}
{{- .Values.fullname | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.name -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "matchd-frontend.version" -}}
{{- .Values.version | default "Unknown" | trunc 63 -}}
{{- end -}}

{{- define "matchd-frontend.environment" -}}
{{- .Values.environment | default "Unknown" | trunc 63 -}}
{{- end -}}

{{/*
Allow for the ability to override the release name used as a label in many places.
*/}}
{{- define "matchd-frontend.releaseLabel" -}}
{{- .Values.releaseLabel | default .Release.Name | trunc 63 -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "matchd-frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the appropriate apiVersion for deployment.
*/}}
{{- define "deployment.apiVersion" -}}
{{- if semverCompare ">=1.9-0" .Capabilities.KubeVersion.GitVersion -}}
{{- print "apps/v1" -}}
{{- else -}}
{{- print "extensions/v1beta1" -}}
{{- end -}}
{{- end -}}

{{/*
Get a hostname from URL
*/}}
{{- define "hostname" -}}
{{- . | trimPrefix "http://" |  trimPrefix "https://" | trimSuffix "/" | quote -}}
{{- end -}}
