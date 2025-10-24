# issue-auth-tool

<details>
<summary>工作流程</summary>

1. **判断类型**

    - 检查该 Issue / Discussion 是否属于以下三类之一：

      - `del`
      - `outdate`
      - `alias`

    - 若属于其中之一，请让 LLM 输出它**打算执行的 MCP 指令**，以便后续验证。

2. **验证 MCP 指令合法性**

    - 检查 LLM 输出的命令是否符合预期格式与安全规则。

3. **执行命令**

    - 若命令合法：执行对应的 MCP 指令，获取所需信息。
    - 若命令不合法：暂停执行，并提示用户**手动修改命令**。

4. **结果验证**

    - 将获取到的信息与原始 Issue / Discussion 内容一并发送给 LLM。
    - 让 LLM 判断其推断是否正确：

           - 若判断正确 → 输出 `del` / `outdate` / `alias` 中的一项。
           - 若判断错误 → 提供错误原因。

<details>
<summary>流程图</summary>

```mermaid


flowchart TD
  Start([开始])
  CheckType{是否为 del / outdate / alias？}
  Terminate([终止 — 非 del/outdate/alias])
  AskLLM[要求 LLM 输出它想要的 MCP 指令]
  Validate{MCP 指令是否合法？}
  Pause([暂停：要求用户修正 MCP 指令])
  Execute[执行合法的 MCP 指令并获取信息]
  Merge[将获取的信息与 issue/discussion 内容合并并发送给 LLM]
  Judge{判定：LLM判定是否正确}
  OutputDecision[输出：del / outdate / alias（任选其一）]
  OutputReason[输出不正确的理由]
  End([结束])

  Start --> CheckType
  CheckType -- 否 --> Terminate
  CheckType -- 是 --> AskLLM
  AskLLM --> Validate
  Validate -- 否 --> Pause
  Pause --> Validate
  Validate -- 是 --> Execute
  Execute --> Merge
  Merge --> Judge
  Judge -- 对 --> OutputDecision --> End
  Judge -- 不对 --> OutputReason --> End

```

</details>
</details>
